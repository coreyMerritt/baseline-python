#!/usr/bin/env python3
import os
import re
from dataclasses import dataclass
from pathlib import Path
from subprocess import CompletedProcess, run
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


# Functions
def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  classes = get_classes(source_paths)
  assert_all_classes_are_imported(classes, source_paths)
  print("All classes are imported. Success.")
  print("Return 0")
  return 0

def ensure_in_project_root() -> None:
  project_root = get_project_root()
  os.chdir(project_root)

def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")

def get_source_paths() -> List[str]:
  cmd_return = bash('find ./src/ -type f | grep -v "__pycache__" | grep -F ".py" | grep -v "__init__"')
  source_paths_blob = str(cmd_return.stdout)
  source_paths_list = source_paths_blob.split("\n")
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

def bash(cmd_str: str) -> CompletedProcess:
  return run(
    args=cmd_str,
    capture_output=True,
    check=True,
    shell=True,
    text=True
  )


# Entrypoint
if __name__ == "__main__":
  main()
