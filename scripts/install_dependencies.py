#!/usr/bin/env python3
import os
import sys
import subprocess


def install_dependencies(
  install_dev: bool | None = None,
  install_infra: bool | None = None
):
  pip_install_args = ["."]
  if install_dev:
    pip_install_args.append(".[dev]")
  else:
    if needs_dev_dependencies():
      pip_install_args.append(".[dev]")
  if install_infra:
    pip_install_args.append(".[infra]")
  else:
    if needs_infra_dependencies():
      pip_install_args.append(".[infra]")
  __pip_install("--upgrade", "pip", "setuptools", "wheel")
  __pip_install(pip_install_args)
  if ".[dev]" in pip_install_args:
    __install_precommit()

def needs_dev_dependencies():
  from dotenv import load_dotenv   # type: ignore   # pylint: disable=import-outside-toplevel,import-error
  load_dotenv()
  ENVIRONMENT = os.getenv("PROJECTNAME_ENVIRONMENT")
  assert ENVIRONMENT
  return ENVIRONMENT.lower() == "dev"

def needs_infra_dependencies():
  return True

def __pip_install(*args):
  cmd = [sys.executable, "-m", "pip", "install", *args]
  subprocess.run(cmd, check=True)

def __install_precommit(*args):
  cmd = ["pre-commit", "install", *args]
  subprocess.run(cmd, check=True)


if __name__ == "__main__":
  install_dependencies()
