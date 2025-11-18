#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_classes, get_source_paths


def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  classes = get_classes(source_paths)
  assert_all_classes_are_imported(classes, source_paths)
  print("All classes are imported. Success.")
  print("Return 0")
  return 0

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


if __name__ == "__main__":
  main()
