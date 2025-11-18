#!/usr/bin/env python3
import re
from typing import List

from system._helpers import Class, ensure_in_project_root, get_classes, get_source_paths


def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  classes = get_classes(source_paths)
  assert_all_classes_are_implemented(classes)
  print("All classes are implemented. Success.")
  print("Return 0")
  return 0

def assert_all_classes_are_implemented(classes: List[Class]):
  for class_ in classes:
    assert is_implemented(class_), f"Never Implemented:\n\t{class_.name}\n\t{class_.path}"

def is_implemented(class_: Class) -> bool:
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for i, line in enumerate(lines):
    line_is_class_match = re.match(fr"^class {class_.name}", line)
    if line_is_class_match:
      line_contains_unimplemented = re.match(r"^\s*(pass|\.\.\.)\s*$", line)
      try:
        next_line_contains_unimplemented = re.match(r"^\s*(pass|\.\.\.)\s*$", lines[i+1])
      except IndexError:
        next_line_contains_unimplemented = None
      if line_contains_unimplemented or next_line_contains_unimplemented:
        return False
  return True


if __name__ == "__main__":
  main()
