import argparse
import sys

from composition.webserver.uvicorn_entrypoint import run_webserver
from interfaces.command_line.enums.run_target import RunTarget
from interfaces.command_line.enums.sub_command import SubCommand
from interfaces.command_line.exceptions.unknown_command_exception import UnknownCommandException
from interfaces.command_line.exceptions.unknown_run_target_exception import UnknownRunTargetException


def entrypoint():
  _add_default_commands()
  args = _build_args()
  _handle_args_routing(args)

def _add_default_commands() -> None:
  if len(sys.argv) == 1:
    sys.argv = [sys.argv[0], "run", "server"]

def _build_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(prog="projectname")
  subparsers = parser.add_subparsers(dest="command", required=True)
  run_parser = subparsers.add_parser(SubCommand.RUN.value)
  run_subparsers = run_parser.add_subparsers(dest="target", required=True)
  server_parser = run_subparsers.add_parser(RunTarget.SERVER.value)
  server_parser.add_argument(
    "--host",
    default=None,
    help="Host address to bind to",
    required=False,
    type=str
  )
  server_parser.add_argument(
    "--port",
    default=None,
    help="Host port to bind to",
    required=False,
    type=int
  )
  args = parser.parse_args()
  return args

def _handle_args_routing(args: argparse.Namespace) -> None:
  if args.command.lower() == SubCommand.RUN.value:
    if args.target.lower() == RunTarget.SERVER.value:
      run_webserver(args.host, args.port)
    else:
      raise UnknownRunTargetException()
  else:
    raise UnknownCommandException()


if __name__ == "__main__":
  entrypoint()
