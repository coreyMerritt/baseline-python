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

def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")
