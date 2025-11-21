#!/usr/bin/env python3
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List


# Classes
@dataclass
class Class:
  name: str
  path: str
  filename: str
  filestem: str

@dataclass
class Module:
  path: str
  filename: str
  filestem: str

class BashError(Exception):
  message: str


# Public Functions
def debug(message: str) -> None:
  print(f"[DEBUG] {message}")

def info(message: str) -> None:
  print(f" [INFO] {message}")

def warn(message: str) -> None:
  print(f" [WARN] {message}")

def error(message: str) -> None:
  print(f"[ERROR] {message}")

def critical(message: str) -> None:
  print(f"\n\t[CRITICAL] {message}\n")
  sys.exit(1)

def ensure_in_project_root() -> None:
  project_root = get_project_root()
  os.chdir(project_root)

def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")

def get_source_paths(
  layer: str | None = None,
  max_depth: int = 99
) -> List[str]:
  source_code_dir = "./src"
  if layer:
    source_code_dir = f"{source_code_dir}/{layer}"
  source_code_dir = f"{source_code_dir}/"
  maxdepth = f"-maxdepth {max_depth}"
  cmd_return = bash(
    f"find {source_code_dir} {maxdepth} -type f \
      | grep -v \"__pycache__\" \
      | grep -F \".py\" \
      | grep -v \"__init__\""
  )
  source_paths_list = cmd_return.split("\n")
  source_paths_list.remove("")
  return source_paths_list

def assert_all_classes_are_imported(classes: List[Class], source_paths: List[str]):
  for class_ in classes:
    assert is_imported_from_some_path(class_, source_paths), f"Never Imported:\n\t{class_.name}\n\t{class_.path}"

def is_imported_from_some_path(class_: Class, source_paths: List[str]) -> bool:
  for source_path in source_paths:
    if is_imported_from_specific_path(class_, source_path):
      return True
  return False

def is_imported_from_specific_path(class_: Class, source_path: str) -> bool:
  with open(source_path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for line in lines:
    match = re.match(fr"^from\ .+\ import\ ({class_.name})(?:,|\s|$)", line)
    if match:
      return True
  return False

def get_errors(paths: List[str]) -> List[Class]:
  error_list = []
  for path in paths:
    try:
      error_name = _get_error_name(path)
      error_path = path
      error_filename = get_filename(path)
      error_filestem = get_filestem(path)
      error_ = Class(
        name=error_name,
        path=error_path,
        filename=error_filename,
        filestem=error_filestem
      )
      error_list.append(error_)
    except ValueError:
      continue
  return error_list

def get_classes(paths: List[str]) -> List[Class]:
  class_list = []
  for path in paths:
    try:
      class_name = get_class_name(path)
      class_path = path
      class_filename = get_filename(path)
      class_filestem = get_filestem(path)
      class_ = Class(
        name=class_name,
        path=class_path,
        filename=class_filename,
        filestem=class_filestem
      )
      class_list.append(class_)
    except ValueError:
      continue
  return class_list

def get_modules(paths: List[str]) -> List[Module]:
  modules_list = []
  for path in paths:
    try:
      get_class_name(path)
      continue
    except ValueError:
      module_path = path
      module_filename = get_filename(path)
      module_filestem = get_filestem(path)
      module = Module(
        path=module_path,
        filename=module_filename,
        filestem=module_filestem
      )
      modules_list.append(module)
  return modules_list

def get_class_name(path: str) -> str:
  match = None
  class_name = None
  with open(path, "r", encoding="utf-8") as class_file:
    lines = class_file.readlines()
  for line in lines:
    match = re.match(r"^class ([A-Z][a-zA-Z]+)[:(]", line)
    if match:
      break
  if match:
    class_name = match.group(1)
  if class_name:
    return class_name
  raise ValueError("No class found")

def get_filename(path: str) -> str:
  return os.path.basename(path)

def get_filestem(path: str) -> str:
  return Path(path).stem

def bash(cmd_str: str) -> str:
  try:
    return run(
      args=cmd_str,
      capture_output=True,
      check=True,
      shell=True,
      text=True
    ).stdout
  except CalledProcessError as e:
    message = "Bash call failed with:"
    message += f"\tSTDOUT: {e.stdout}"
    message += f"\tSTDERR: {e.stderr}"
    raise BashError(message) from e

def _get_error_name(path: str) -> str:
  match = None
  error_name = None
  with open(path, "r", encoding="utf-8") as error_file:
    lines = error_file.readlines()
  for line in lines:
    err_match = re.match(r"^class ([A-Z][a-zA-Z]+Err)[:(]", line)
    if err_match:
      match = err_match
      break
    error_match = re.match(r"^class ([A-Z][a-zA-Z]+Error)[:(]", line)
    if error_match:
      match = error_match
      break
    exc_match = re.match(r"^class ([A-Z][a-zA-Z]+Exc)[:(]", line)
    if exc_match:
      match = exc_match
      break
    exception_match = re.match(r"^class ([A-Z][a-zA-Z]+Exception)[:(]", line)
    if exception_match:
      match = exception_match
      break
  if match:
    error_name = match.group(1)
  if error_name:
    return error_name
  raise ValueError("Not an exception")
