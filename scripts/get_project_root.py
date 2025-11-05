#!/usr/bin/env python3
from pathlib import Path


def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")


if __name__ == "__main__":
  get_project_root()
