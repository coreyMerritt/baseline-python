#!/usr/bin/env python3
import json
import os
import time
from sys import argv

import requests
import yaml
from dotenv import load_dotenv

from _helpers import BashError, bash, critical, get_project_name, info

AUTHORITY_URL = "https://login.microsoftonline.com"
GRAPH_URL = "https://graph.microsoft.com/v1.0"
assert len(argv) > 1, "arg1: <deployment_environment>"
assert len(argv) < 3, "Script does not accept 2nd arg."
assert argv[1] in ("dev", "prod", "test"), "arg1: <dev|prod|test>"
DEPLOYMENT_ENVIRONMENT = argv[1]
PROJECTNAME = get_project_name()
AD_APP_NAME = f"{PROJECTNAME.lower()}-{DEPLOYMENT_ENVIRONMENT}-identities"
SECRET_NAME = f"{AD_APP_NAME}-secret"

def set_up_entra_id():
  _ensure_az_installed()
  _ensure_az_logged_in()
  _ensure_ad_access()
  tenant_id = _get_tenant_id()
  config_path = _get_config_path(DEPLOYMENT_ENVIRONMENT)
  if not os.path.exists(config_path):
    if _is_ad_app():
      app_data = _get_existing_ad_app()
    else:
      app_data = _create_ad_app()
    client_id = app_data["appId"]
    _ensure_credentials_do_not_exist(client_id, config_path)
    credentials = _get_new_credentials(client_id)
    client_secret = credentials["password"]
    _create_new_entra_id_config(config_path, client_id, client_secret, tenant_id)
  else:
    info("Config already exists. Skipping creation.")
    config = _get_existing_entra_id_config(config_path)
    client_id = config["client_id"]
  if not _is_app_service_principal(client_id):
    _create_app_service_principal(client_id)
  _validate_config(config_path)
  _test_config_connection(config_path)

def _ensure_az_installed() -> None:
  try:
    bash("az --version")
  except BashError:
    critical("Install the az cli tool and run again.")

def _ensure_az_logged_in() -> None:
  try:
    email = bash("az account show | jq -r .user.name").replace("\n", "")
    info(f"Using current user: {email}")
  except BashError:
    critical("Log in with: az login")

def _ensure_ad_access() -> None:
  bash("az ad user list")

def _get_tenant_id() -> str:
  tenant_id = bash("az account show --query tenantId -o tsv").replace("\n", "")
  info(f"Using current tenant: {tenant_id}")
  return tenant_id

def _get_config_path(deployment_environment: str) -> str:
  load_dotenv()
  if deployment_environment not in ["dev", "prod", "test"]:
    raise AttributeError("deployment_environment must be dev|prod|test")
  global_config_dir = os.getenv("PROJECTNAME_GLOBAL_CONFIG_DIR")
  assert global_config_dir
  entra_id_config_path = f"{global_config_dir}/{deployment_environment}/entra_id.yml"
  return entra_id_config_path

def _is_ad_app() -> bool:
  response_str = bash(f"az ad app list --query \"[?displayName=='{AD_APP_NAME}']\"")
  response_list = json.loads(response_str)
  if len(response_list) == 0:
    return False
  return True

def _get_existing_ad_app() -> dict:
  response_str = bash(f"az ad app list --query \"[?displayName=='{AD_APP_NAME}']\"")
  response_list = json.loads(response_str)
  assert len(response_list) > 0, "Logic error: Function should not be called without first ensuring an app exists."
  assert len(response_list) < 2, f"Multiple apps found matching name: {AD_APP_NAME}"
  return response_list[0]

def _create_ad_app() -> dict:
  info("Creating AD APP...")
  response_str = bash(f"""
    az ad app create \
      --display-name "{AD_APP_NAME}" \
      --enable-id-token-issuance true \
      --enable-access-token-issuance true
  """)
  response_dict = json.loads(response_str)
  return response_dict

def _is_app_service_principal(client_id: str) -> bool:
  try:
    bash(f"az ad sp show --id \"{client_id}\"")
    return True
  except BashError:
    return False

def _create_app_service_principal(client_id: str) -> None:
  bash(f"az ad sp create --id \"{client_id}\"")

def _ensure_credentials_do_not_exist(client_id: str, config_path: str) -> None:
  all_app_credentials_str = bash(f"az ad app show --id \"{client_id}\" --query passwordCredentials")
  all_app_credentials_list = json.loads(all_app_credentials_str)
  for credentials in all_app_credentials_list:
    if credentials["displayName"] == SECRET_NAME:
      critical(f"""Credentials already exist: {SECRET_NAME}
          Either insert a config at: {config_path}
            OR
          Remove existing credentials with:
            az ad app credential delete --id "{client_id}" --key-id "{credentials["keyId"]}"
      """)

def _get_new_credentials(client_id: str) -> dict:
  response_str = bash(f"""\
    az ad app credential reset \
      --id "{client_id}" \
      --display-name "{SECRET_NAME}"
  """)
  response_dict = json.loads(response_str)
  return response_dict

def _get_existing_entra_id_config(config_path: str) -> dict:
  with open(config_path, "r", encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)
  return config

def _create_new_entra_id_config(
  entra_id_config_path: str,
  client_id: str,
  client_secret: str,
  tenant_id: str,
) -> None:
  new_config = {
    "tenant_id": tenant_id,
    "client_id": client_id,
    "client_secret": client_secret,
    "authority_url": AUTHORITY_URL,
    "graph_url": GRAPH_URL
  }
  with open(entra_id_config_path, "w", encoding='utf-8') as config_file:
    yaml.safe_dump(new_config, config_file)
  info(f"New config: {entra_id_config_path}")

def _validate_config(config_path: str) -> None:
  with open(config_path, "r", encoding="utf-8") as config_file:
    config_dict = yaml.safe_load(config_file)
  assert config_dict["tenant_id"]
  assert config_dict["client_id"]
  assert config_dict["client_secret"]
  assert config_dict["authority_url"]
  assert config_dict["graph_url"]

def _test_config_connection(config_path: str) -> None:
  with open(config_path, "r", encoding="utf-8") as config_file:
    config_dict = yaml.safe_load(config_file)
  tenant_id = config_dict["tenant_id"]
  client_id = config_dict["client_id"]
  client_secret = config_dict["client_secret"]
  info("Testing credentials. This may take a moment...")
  timeout = 60
  rc = -1
  start_time = time.time()
  while rc != 200 and time.time() - start_time < timeout:
    response = requests.post(
      url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
      data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://management.azure.com/.default"
      },
      timeout=15
    )
    rc = response.status_code
    time.sleep(1)
  assert response.status_code == 200
  info("Connection successful.")


if __name__ == "__main__":
  set_up_entra_id()
