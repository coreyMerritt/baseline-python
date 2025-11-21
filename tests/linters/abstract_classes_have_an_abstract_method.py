#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_filename, get_filestem, get_source_paths


def main():
  ensure_in_project_root()
  source_paths = get_source_paths()
  abstract_classes = get_abstract_classes(source_paths)
  for abstract_class in abstract_classes:
    print(abstract_class.name)
  assert_all_abstract_classes_have_abstract_methods(abstract_classes)
  print("0: All abstract classes have at least one abstract method.")
  return 0

def assert_all_abstract_classes_have_abstract_methods(abstract_classes: List[Class]):
  for class_ in abstract_classes:
    fail_message = f"Abstract class doesn't contain abstract method:\n\t{class_.name}\n\t{class_.path}"
    assert has_abstract_method(class_), fail_message

def has_abstract_method(class_: Class) -> bool:
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    abstract_method_match = re.search(r"@abstractmethod", line)
    if abstract_method_match:
      return True
  return False

def get_abstract_classes(paths: List[str]) -> List[Class]:
  abstract_class_list = []
  for path in paths:
    try:
      abstract_class_name = get_abstract_class_name(path)
      abstract_class_path = path
      abstract_class_filename = get_filename(path)
      abstract_class_filestem = get_filestem(path)
      abstract_class = Class(
        name=abstract_class_name,
        path=abstract_class_path,
        filename=abstract_class_filename,
        filestem=abstract_class_filestem
      )
      abstract_class_list.append(abstract_class)
    except ValueError:
      continue
  return abstract_class_list

def get_abstract_class_name(path: str) -> str:
  match = None
  abstract_class_name = None
  with open(path, "r", encoding="utf-8") as abstract_class_file:
    lines = abstract_class_file.readlines()
  for line in lines:
    match = re.match(r"^class ([A-Z][a-zA-Z]+)\(ABC\):", line)
    if match:
      break
  if match:
    abstract_class_name = match.group(1)
  if abstract_class_name:
    return abstract_class_name
  raise ValueError("Not an abstract class")

if __name__ == "__main__":
  main()
