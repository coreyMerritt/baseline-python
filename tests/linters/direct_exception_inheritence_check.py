#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_filename, get_filestem, get_source_paths

EXCEPTION_LIST = [
  "ProjectnameException",
  "ProjectnameHTTPException"
]

def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  errors = get_errors(source_paths)
  assert_all_errors_dont_inherit_from_exception(errors)
  print("All errors do not inherit from Exception.")
  print("Return 0")
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

def get_errors(paths: List[str]) -> List[Class]:
  error_list = []
  for path in paths:
    try:
      error_name = get_error_name(path)
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

def get_error_name(path: str) -> str:
  match = None
  error_name = None
  with open(path, "r", encoding="utf-8") as error_file:
    lines = error_file.readlines()
  for line in lines:
    err_match = re.match(r"^error ([A-Z][a-zA-Z]+Err)[:(]", line)
    if err_match:
      match = err_match
      break
    error_match = re.match(r"^error ([A-Z][a-zA-Z]+Error)[:(]", line)
    if error_match:
      match = error_match
      break
    exc_match = re.match(r"^error ([A-Z][a-zA-Z]+Exc)[:(]", line)
    if exc_match:
      match = exc_match
      break
    exception_match = re.match(r"^error ([A-Z][a-zA-Z]+Exception)[:(]", line)
    if exception_match:
      match = exception_match
      break
  if match:
    error_name = match.group(1)
  if error_name:
    return error_name
  raise ValueError("Not an exception")


if __name__ == "__main__":
  main()
