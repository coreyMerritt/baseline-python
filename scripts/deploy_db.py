#!/usr/bin/env python3
import os
import sys
import secrets
import string
import time

import docker
import yaml
import psycopg

from utilities.get_project_name import get_project_name
from utilities.get_project_root import get_project_root


def deploy_db() -> None:
  __require_sudo()
  if not sys.argv[1]:
    print("\n\targ1 must be arg1 must be test|dev|prod\n")
  PROJECT_ENVIRONMENT = sys.argv[1]
  print(f"Environment: {PROJECT_ENVIRONMENT}")
  PROJECT_NAME = get_project_name()
  PROJECT_ROOT = get_project_root()
  DB_CONFIG_PATH = f"{PROJECT_ROOT}/config/{PROJECT_ENVIRONMENT}/database.yml"
  POSTGRES_USERNAME = f"{PROJECT_NAME}-user"
  POSTGRES_PASSWORD = __generate_password(16)
  POSTGRES_DBNAME = f"{PROJECT_NAME}-{PROJECT_ENVIRONMENT}"
  if PROJECT_ENVIRONMENT == "test":
    HOST_PORT = 5434
  elif PROJECT_ENVIRONMENT == "dev":
    HOST_PORT = 5433
  elif PROJECT_ENVIRONMENT == "prod":
    HOST_PORT = 5432
  else:
    raise RuntimeError(f"Unknown environment: {PROJECT_ENVIRONMENT}")
  IMAGE_VERSION = "18"
  CONTAINER_NAME = f"postgres-{IMAGE_VERSION}-{PROJECT_NAME}-{PROJECT_ENVIRONMENT}"
  created_new_config = False
  if PROJECT_ENVIRONMENT == "test" or PROJECT_ENVIRONMENT == "dev":
    __create_new_config(
      new_config_path=DB_CONFIG_PATH,
      port=HOST_PORT,
      dbname=POSTGRES_DBNAME,
      username=POSTGRES_USERNAME,
      password=POSTGRES_PASSWORD
    )
    created_new_config=True

  CLIENT = docker.from_env()
  for container in CLIENT.containers.list(all=True):
    if container.name == CONTAINER_NAME:
      print(f"Stopping container: {container.name}")
      container.stop()
      print(f"Removing container: {container.name}")
      container.remove()
      break
  print(f"Running container: {CONTAINER_NAME}")
  if PROJECT_ENVIRONMENT == "prod":
    container = CLIENT.containers.run(
      detach=True,
      remove=False,
      name=CONTAINER_NAME,
      environment={
        "POSTGRES_DB": POSTGRES_DBNAME,
        "POSTGRES_USER": POSTGRES_USERNAME,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD
      },
      ports={
        "5432/tcp": HOST_PORT
      },
      volumes={
        f"{CONTAINER_NAME}-volume": {
          "bind": "/var/lib/postgresql",
          "mode": "rw",
        }
      },
      image=f"postgres:{IMAGE_VERSION}"
    )
  else:
    container = CLIENT.containers.run(
      detach=True,
      remove=False,
      name=CONTAINER_NAME,
      environment={
        "POSTGRES_DB": POSTGRES_DBNAME,
        "POSTGRES_USER": POSTGRES_USERNAME,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD
      },
      ports={
        "5432/tcp": HOST_PORT
      },
      image=f"postgres:{IMAGE_VERSION}"
    )
  print("\npsql \\")
  print("  --host=127.0.0.1 \\")
  print(f"  --port={HOST_PORT} \\")
  print(f"  --dbname={POSTGRES_DBNAME} \\")
  print(f"  --username={POSTGRES_USERNAME}\n")
  if created_new_config:
    print(f"Created new config with creds at: {DB_CONFIG_PATH}")
  else:
    print("Host: 127.0.0.1")
    print(f"Port: {HOST_PORT}")
    print(f"Database Name: {POSTGRES_DBNAME}")
    print(f"Username: {POSTGRES_USERNAME}")
    print(f"Password: {POSTGRES_PASSWORD}")
  print()
  __wait_for_healthy_db(
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    dbname=POSTGRES_DBNAME,
    port=HOST_PORT,
    host="127.0.0.1",
    timeout=15
  )
  print()


def __require_sudo():
  if os.geteuid() != 0:
    print("Run with sudo.")
    sys.exit(1)

def __generate_password(length: int) -> str:
  print("Generating password...")
  alphabet = string.ascii_letters + string.digits
  return ''.join(secrets.choice(alphabet) for _ in range(length))

def __create_new_config(new_config_path: str, port: int, dbname: str, username: str, password: str) -> None:
  print(f"New config: {new_config_path}")
  new_config = {
    "engine": "postgresql",
    "host": "127.0.0.1",
    "port": port,
    "name": dbname,
    "username": username,
    "password": password
  }
  with open(new_config_path, "w", encoding='utf-8') as config_file:
    yaml.safe_dump(new_config, config_file)

def __wait_for_healthy_db(user, password, dbname, port, host="localhost", timeout=15):
  print("Waiting for database to become healthy...")
  start = time.time()
  while time.time() - start < timeout:
    try:
      with psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        connect_timeout=2,
      ):
        print("Confirmed database is healthy.")
        return
    except psycopg.OperationalError:
      time.sleep(1)
  raise TimeoutError("Timed out waiting for database health.")


if __name__ == "__main__":
  deploy_db()
