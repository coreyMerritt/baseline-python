#!/usr/bin/env python3
import tomllib
from pathlib import Path


def get_project_name() -> str:
  pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
  with pyproject_path.open("rb") as f:
    data = tomllib.load(f)
  if "project" in data and "name" in data["project"]:
    return data["project"]["name"]
  if "tool" in data and "poetry" in data["tool"] and "name" in data["tool"]["poetry"]:
    return data["tool"]["poetry"]["name"]
  raise KeyError("Project name not found in pyproject.toml")


if __name__ == "__main__":
  print(get_project_name())
