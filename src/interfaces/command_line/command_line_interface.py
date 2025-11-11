import argparse
import sys

from interfaces.command_line.enums.command import Command
from interfaces.command_line.enums.run_target import RunTarget
from interfaces.command_line.exceptions.unknown_command_exception import UnknownCommandException
from interfaces.command_line.exceptions.unknown_run_target_exception import UnknownRunTargetException
from interfaces.rest.run_server import run_server


class CommandLineInterface:
  def run(self):
    # Default
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
      sys.argv = [sys.argv[0], "run", "server", sys.argv[1]]
    # Give the interface enough info to give a helpful error
    elif len(sys.argv) == 1:
      sys.argv = [sys.argv[0], "run", "server"]
    parser = argparse.ArgumentParser(prog="PROJECTNAME")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser(Command.RUN.value)
    run_subparsers = run_parser.add_subparsers(dest="target", required=True)
    server_parser = run_subparsers.add_parser(RunTarget.SERVER.value)
    server_parser.add_argument("env", help="Environment: dev|test|prod")
    server_parser.add_argument("--host", default="0.0.0.0")
    server_parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command.lower() == Command.RUN.value:
      if args.target.lower() == RunTarget.SERVER.value:
        run_server(args.env, args.host, args.port)
      else:
        raise UnknownRunTargetException()
    else:
      raise UnknownCommandException()
