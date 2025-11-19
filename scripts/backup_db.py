#!/usr/bin/env python3
import sys

from _helpers import backup_db, critical, require_sudo

if __name__ == "__main__":
  require_sudo()
  if not sys.argv[1]:
    critical("\n\targ1 must be dev|prod|test\n")
  DEPLOYMENT_ENVIRONMENT = sys.argv[1]
  backup_db(DEPLOYMENT_ENVIRONMENT)
