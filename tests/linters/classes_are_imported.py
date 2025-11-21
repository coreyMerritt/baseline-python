#!/usr/bin/env python3
from linters._helpers import assert_all_classes_are_imported, ensure_in_project_root, get_classes, get_source_paths


def main():
  ensure_in_project_root()
  source_paths = get_source_paths(base_dir="./src/")
  classes = get_classes(source_paths)
  assert_all_classes_are_imported(classes, source_paths)
  print("0: All classes are imported.")
  return 0


if __name__ == "__main__":
  main()
