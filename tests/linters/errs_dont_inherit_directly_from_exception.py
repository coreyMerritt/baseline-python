#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_errors, get_source_paths

EXCEPTION_LIST = [
  "ProjectnameException",
  "ProjectnameHTTPException"
]

def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  errors = get_errors(source_paths)
  assert_all_errors_dont_inherit_from_exception(errors)
  print("0: All errors do not inherit from Exception.")
  return 0

def assert_all_errors_dont_inherit_from_exception(errors: List[Class]):
  for error in errors:
    if error.name not in EXCEPTION_LIST:
      assert not inherits_from_exception(error), f"Inherits from Exception:\n\t{error.name}\n\t{error.path}"

def inherits_from_exception(error: Class) -> bool:
  with open(error.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    line_is_error_definition = re.match(fr"error {error.name}", line)
    if line_is_error_definition:
      inherits_from_exc = re.search(r"\(Exception\):", line)
      if inherits_from_exc:
        return True
  return False


if __name__ == "__main__":
  main()
