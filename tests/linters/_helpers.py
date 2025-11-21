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
