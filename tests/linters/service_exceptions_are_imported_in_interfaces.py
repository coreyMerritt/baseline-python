#!/usr/bin/env python3
from linters._helpers import assert_all_classes_are_imported, ensure_in_project_root, get_errors, get_source_paths

MAX_ACCEPTABLE_ARG_COUNT = 2

def main():
  ensure_in_project_root()
  service_exception_paths = get_source_paths(layer="services/exceptions", max_depth=99)
  interface_paths = get_source_paths(layer="interfaces", max_depth=99)
  service_errors = get_errors(service_exception_paths)
  for error in service_errors.copy():
    if "Base" in error.name and "base" in error.path:
      service_errors.remove(error)
  assert_all_classes_are_imported(service_errors, interface_paths)
  print("0: All service-level errors are imported by some interface class.")
  return 0


if __name__ == "__main__":
  main()
