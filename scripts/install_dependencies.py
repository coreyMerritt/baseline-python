#!/usr/bin/env python3
import os
import sys
import subprocess


def install_core_dependencies():
  __pip_install("--upgrade", "pip", "setuptools", "wheel")
  __pip_install(".")

def install_dev_dependencies():
  __pip_install(".[dev]")
  __install_precommit()

def install_infra_dependencies():
  __pip_install(".[infra]")

def needs_dev_dependencies():
  from dotenv import load_dotenv   # type: ignore   # pylint: disable=import-outside-toplevel,import-error
  load_dotenv()
  ENVIRONMENT = os.getenv("PROJECTNAME_ENVIRONMENT")
  assert ENVIRONMENT
  return ENVIRONMENT.lower() == "dev"

def needs_infra_dependencies():
  from dotenv import load_dotenv   # type: ignore   # pylint: disable=import-outside-toplevel,import-error
  load_dotenv()
  ENVIRONMENT = os.getenv("PROJECTNAME_ENVIRONMENT")
  assert ENVIRONMENT
  return ENVIRONMENT.lower() == "dev" or ENVIRONMENT.lower() == "test"

def __pip_install(*args):
  cmd = [sys.executable, "-m", "pip", "install", *args]
  subprocess.run(cmd, check=True)

def __install_precommit(*args):
  cmd = ["pre-commit", "install", *args]
  subprocess.run(cmd, check=True)


if __name__ == "__main__":
  install_core_dependencies()
  if needs_dev_dependencies():
    install_dev_dependencies()
  if needs_infra_dependencies():
    install_infra_dependencies()
