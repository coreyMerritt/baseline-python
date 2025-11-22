import argparse
import sys

from composition.uvicorn_entrypoint import run_webserver
from interfaces.command_line.enums.run_target import RunTarget
from interfaces.command_line.enums.sub_command import SubCommand
from interfaces.command_line.exceptions.unknown_command_exception import UnknownCommandException
from interfaces.command_line.exceptions.unknown_run_target_exception import UnknownRunTargetException


def entrypoint():
  _add_default_commands()
  args = _build_args()
  _handle_args_routing(args)

def _add_default_commands() -> None:
  if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
    sys.argv = [sys.argv[0], "run", "server", sys.argv[1]]

def _build_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(prog="PROJECTNAME")
  subparsers = parser.add_subparsers(dest="command", required=True)
  run_parser = subparsers.add_parser(SubCommand.RUN.value)
  run_subparsers = run_parser.add_subparsers(dest="target", required=True)
  server_parser = run_subparsers.add_parser(RunTarget.SERVER.value)
  server_parser.add_argument("env", help="Environment: dev|test|prod")
  server_parser.add_argument("--host", default="0.0.0.0")
  server_parser.add_argument("--port", type=int, default=8000)
  args = parser.parse_args()
  return args

def _handle_args_routing(args: argparse.Namespace) -> None:
  if args.command.lower() == SubCommand.RUN.value:
    if args.target.lower() == RunTarget.SERVER.value:
      run_webserver(args.env, args.host, args.port)
    else:
      raise UnknownRunTargetException()
  else:
    raise UnknownCommandException()


if __name__ == "__main__":
  entrypoint()
