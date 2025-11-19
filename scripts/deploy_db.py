#!/usr/bin/env python3
import sys
import time

import docker
import psycopg
import yaml
from docker import DockerClient
from docker.errors import APIError
from docker.models.containers import Container

from _helpers import (PostgresInfo, backup_db, critical, debug, docker_volume_exists, filesystem_log,
                      generate_new_database_info, get_existing_database_info, info, is_docker_container_running,
                      output_seperator, require_sudo, warn)

LOG_PATH = "./deploy_db.log"
IMAGE_VERSION = "18"

def deploy_db() -> None:
  require_sudo()
  if not sys.argv[1]:
    critical("arg1 must be dev|prod|test")
  DEPLOYMENT_ENVIRONMENT = sys.argv[1]
  debug(f"Environment: {DEPLOYMENT_ENVIRONMENT}")
  client = docker.from_env()
  container_name = generate_new_database_info(DEPLOYMENT_ENVIRONMENT).container_name
  volume_name = f"{container_name}-volume"
  if is_docker_container_running(container_name, client):
    backup_db(DEPLOYMENT_ENVIRONMENT)
  else:
    warn(f"Couldn't find database to backup: {container_name}")
    warn("Waiting 15s to allow user to abort, then proceeding without a backup...")
    time.sleep(15)
  if DEPLOYMENT_ENVIRONMENT == "prod":
    if docker_volume_exists(volume_name, client):
      _deploy_with_existing_volume(volume_name, DEPLOYMENT_ENVIRONMENT, client)
    else:
      _deploy_with_new_volume(volume_name, DEPLOYMENT_ENVIRONMENT, client)
  else:
    if docker_volume_exists(volume_name, client):
      assert "prod" not in DEPLOYMENT_ENVIRONMENT, "TRYING TO REMOVE PROD VOLUME. ABORTING."
      assert "prod" not in volume_name, "TRYING TO REMOVE PROD VOLUME. ABORTING."
      container_name = generate_new_database_info(DEPLOYMENT_ENVIRONMENT).container_name
      _stop_and_remove_container(client, container_name)
      _remove_docker_volume(volume_name, client)
    _deploy_with_new_volume(volume_name, DEPLOYMENT_ENVIRONMENT, client)

def _deploy_with_existing_volume(volume_name: str, deployment_environment: str, client: DockerClient) -> None:
  postgres_info = get_existing_database_info(deployment_environment, IMAGE_VERSION)
  _deploy_with_defined_volume(
    volume_name,
    postgres_info,
    client
  )

def _deploy_with_new_volume(volume_name: str, deployment_environment: str, client: DockerClient) -> None:
  postgres_info = generate_new_database_info(deployment_environment)
  _create_new_project_database_config(postgres_info)
  _deploy_with_defined_volume(
    volume_name,
    postgres_info,
    client
  )
  info(f"Created new config with creds at: {postgres_info.config_path}")

def _deploy_with_defined_volume(
  volume_name: str,
  postgres_info: PostgresInfo,
  client: DockerClient
) -> None:
  _stop_and_remove_container(client, postgres_info.container_name)
  info(f"Running container: {postgres_info.container_name}")
  try:
    container = _run_container_with_volume_mount(volume_name, client, postgres_info)
  except APIError as e:
    if "port is already allocated" not in str(e):
      raise e
    critical(f"Failed to deploy container because port {postgres_info.host_port} is in use... Aborting.")
  container.reload()
  _output_logs(volume_name, postgres_info)
  _wait_for_healthy_db(postgres_info)

def _create_new_project_database_config(postgres_info: PostgresInfo) -> None:
  info(f"New config: {postgres_info.config_path}")
  new_config = {
    "engine": "postgresql",
    "host": "127.0.0.1",
    "port": postgres_info.host_port,
    "name": postgres_info.db_name,
    "username": postgres_info.username,
    "password": postgres_info.password
  }
  with open(postgres_info.config_path, "w", encoding='utf-8') as config_file:
    yaml.safe_dump(new_config, config_file)

def _stop_and_remove_container(client: DockerClient, container_removal_name: str) -> None:
  for container in client.containers.list(all=True):
    if container.name == container_removal_name:
      info(f"Stopping container: {container.name}")
      container.stop()
      info(f"Removing container: {container.name}")
      container.remove()
      break

def _remove_docker_volume(volume_name: str, client: DockerClient) -> None:
  debug(f"Removing docker volume: {volume_name}")
  assert "prod" not in volume_name, "TRYING TO REMOVE PROD VOLUME. ABORTING."
  volume = client.volumes.get(volume_name)
  volume.remove(force=True)

def _output_logs(volume_name: str, postgres_info: PostgresInfo) -> None:
  output_seperator()
  _output_container_info(volume_name, postgres_info)
  output_seperator()
  _output_psql_helper(postgres_info)
  output_seperator()
  _output_database_info(postgres_info)
  output_seperator()
  filesystem_log("=" * 120, LOG_PATH)

def _run_container_with_volume_mount(volume_name: str, client: DockerClient, postgres_info: PostgresInfo) -> Container:
  return client.containers.run(
    detach=True,
    remove=False,
    name=postgres_info.container_name,
    environment={
      "POSTGRES_DB": postgres_info.db_name,
      "POSTGRES_USER": postgres_info.username,
      "POSTGRES_PASSWORD": postgres_info.password
    },
    ports={
      "5432/tcp": postgres_info.host_port
    },
    volumes={
      volume_name: {
        "bind": "/var/lib/postgresql",
        "mode": "rw",
      }
    },
    image=f"postgres:{postgres_info.image_version}"
  )

def _output_psql_helper(postgres_info: PostgresInfo) -> None:
  print("Command-line access:")
  print("  psql \\")
  print("    --host=127.0.0.1 \\")
  print(f"    --port={postgres_info.host_port} \\")
  print(f"    --dbname={postgres_info.db_name} \\")
  print(f"    --username={postgres_info.username}")

def _output_database_info(postgres_info: PostgresInfo) -> None:
  print("Database Info:")
  print( "           Host: 127.0.0.1")
  print(f"           Port: {postgres_info.host_port}")
  print(f"  Database Name: {postgres_info.db_name}")
  print(f"       Username: {postgres_info.username}")
  print(f"       Password: {postgres_info.password}")
  filesystem_log("Host: 127.0.0.1", LOG_PATH)
  filesystem_log(f"Port: {postgres_info.host_port}", LOG_PATH)
  filesystem_log(f"Database Name: {postgres_info.db_name}", LOG_PATH)
  filesystem_log(f"Username: {postgres_info.username}", LOG_PATH)
  filesystem_log(f"Password: {postgres_info.password}", LOG_PATH)

def _output_container_info(volume_name: str, postgres_info: PostgresInfo) -> None:
  print("Container Info:")
  print(f"      Name: {postgres_info.container_name}")
  print(f"    Volume: {volume_name}")
  filesystem_log(f"Name: {postgres_info.container_name}", LOG_PATH)
  filesystem_log(f"Volume: {volume_name}", LOG_PATH)

def _wait_for_healthy_db(postgres_info: PostgresInfo, host: str = "127.0.0.1"):
  info("Waiting for database to become healthy...")
  timeout = 15
  start = time.time()
  while time.time() - start < timeout:
    try:
      with psycopg.connect(
        dbname=postgres_info.db_name,
        user=postgres_info.username,
        password=postgres_info.password,
        host=host,
        port=postgres_info.host_port,
        connect_timeout=2,
      ):
        info("Confirmed that database is healthy.")
        return
    except psycopg.OperationalError:
      time.sleep(1)
  raise TimeoutError("Timed out waiting for database health.")


if __name__ == "__main__":
  deploy_db()
