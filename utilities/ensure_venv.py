#!/usr/bin/env python3
import os
import subprocess
import sys
import venv
from pathlib import Path
from utilities.get_project_root import get_project_root


VENV_DIR = get_project_root() / ".venv"

def ensure_venv():
  if not VENV_DIR.exists():
    print(f"Creating virtual environment at: {VENV_DIR}")
    venv.create(VENV_DIR, with_pip=True)
    subprocess.run([VENV_DIR / "bin" / "python", "-m", "pip", "install", "-U", "pip"], check=True)
  IN_VENV = Path(sys.prefix).resolve() == VENV_DIR.resolve()
  if not IN_VENV:
    print("Re-executing inside venv...")
    PYTHON_BIN_IN_VENV = VENV_DIR / "bin" / "python"
    os.execv(str(PYTHON_BIN_IN_VENV), [str(PYTHON_BIN_IN_VENV)] + sys.argv)


if __name__ == "__main__":
  ensure_venv()
