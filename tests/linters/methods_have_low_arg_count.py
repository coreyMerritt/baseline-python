#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, debug, ensure_in_project_root, get_classes, get_source_paths, info

MAX_ACCEPTABLE_ARG_COUNT = 2

def main():
  ensure_in_project_root()
  source_paths = get_source_paths(layer="interfaces/rest/health/controllers", max_depth=1)
  source_paths.extend(get_source_paths(layer="interfaces/rest/health/routes", max_depth=1))
  source_paths.extend(get_source_paths(layer="interfaces/rest/v1/controllers", max_depth=1))
  source_paths.extend(get_source_paths(layer="interfaces/rest/v1/routes", max_depth=1))
  source_paths.extend(get_source_paths(layer="infrastructure", max_depth=2))
  source_paths.extend(get_source_paths(layer="services", max_depth=1))
  classes = get_classes(source_paths)
  assert_all_classes_contain_proper_arg_count(classes)
  info("0")
  return 0

def assert_all_classes_contain_proper_arg_count(classes: List[Class]):
  for class_ in classes:
    fail_msg = f"Class method contains too many args:\n\t{class_.name}\n\t{class_.path}"
    assert contains_healthy_arg_count(class_), fail_msg

def contains_healthy_arg_count(class_: Class) -> bool:
  debug(f"Checking class: {class_.name}")
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    method_match = re.search(r"^\s*def\s+\w+\s*\(([^)]*)\)", line)
    if method_match:
      method_name_match = re.search(r"^\s*def\s(.+)\(", line)
      method_name = "Unknown Method"
      if method_name_match:
        method_name = method_name_match.group(1)
      raw_args = method_match.group(1)
      method_parameters = [a.strip() for a in raw_args.split(",") if a.strip()]
      fail_msg = f"Class method contains too many args:\n\t{method_name}\n\t{class_.name}\n\t{class_.path}"
      assert len(method_parameters) <= MAX_ACCEPTABLE_ARG_COUNT + 1, fail_msg
  return True


if __name__ == "__main__":
  main()
