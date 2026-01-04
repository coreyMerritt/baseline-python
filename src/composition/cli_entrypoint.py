import argparse
from dataclasses import asdict
import json
import sys

from composition.models.app_resources import AppResources
from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from composition.resources import get_resources_dict
from composition.webserver.uvicorn_entrypoint import run_webserver
from infrastructure.logger.enums.logger_level import LoggerLevel
from interfaces.command_line.enums.get_target import GetTarget
from interfaces.command_line.enums.run_target import RunTarget
from interfaces.command_line.enums.sub_command import SubCommand
from interfaces.command_line.exceptions.unknown_command_exception import UnknownCommandException
from interfaces.command_line.exceptions.unknown_run_target_exception import UnknownRunTargetException
from services.health_manager import HealthManager


def entrypoint():
  _add_default_commands()
  args = _build_args()
  _handle_args_routing(args)

def _add_default_commands() -> None:
  if len(sys.argv) == 1:
    sys.argv = [sys.argv[0], "run", "server"]

def _build_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(prog="foo-project-name")
  subparsers = parser.add_subparsers(dest="command", required=True)
  get_parser = subparsers.add_parser(SubCommand.GET.value)
  get_subparsers = get_parser.add_subparsers(dest="target", required=True)
  get_subparsers.add_parser(GetTarget.HEALTH_REPORT.value)
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
  if args.command.lower() == SubCommand.GET.value:
    if args.target.lower() == GetTarget.HEALTH_REPORT.value:
      _get_full_health_report()
  elif args.command.lower() == SubCommand.RUN.value:
    if args.target.lower() == RunTarget.SERVER.value:
      run_webserver(args.host, args.port)
    else:
      raise UnknownRunTargetException()
  else:
    raise UnknownCommandException()

def _build_resources() -> AppResources:
  resources_dict = get_resources_dict()
  infra = InfrastructureCollection(
    config_parser=resources_dict["infra"]["config_parser"],
    cpu=resources_dict["infra"]["cpu"],
    database=resources_dict["infra"]["database"],
    disk=resources_dict["infra"]["disk"],
    environment=resources_dict["infra"]["environment"],
    logger=resources_dict["infra"]["logger"],
    memory=resources_dict["infra"]["memory"],
    typicode_client=resources_dict["infra"]["typicode_client"]
  )
  repos = RepositoryCollection(
    account=resources_dict["repos"]["account"],
    blog_post=resources_dict["repos"]["blog_post"],
    membership=resources_dict["repos"]["membership"],
    role=resources_dict["repos"]["role"],
    user=resources_dict["repos"]["user"]
  )
  resources = AppResources(
    infra=infra,
    repos=repos
  )
  return resources

def _get_full_health_report() -> None:
  resources = _build_resources()
  resources.infra.logger.set_level(LoggerLevel.WARNING)
  resources.infra.logger.set_json(False)
  health_manager = HealthManager(
    logger=resources.infra.logger,
    config_parser=resources.infra.config_parser,
    cpu=resources.infra.cpu,
    database=resources.infra.database,
    disk=resources.infra.disk,
    environment=resources.infra.environment,
    memory=resources.infra.memory,
    typicode_client=resources.infra.typicode_client
  )
  health_report_som = health_manager.get_full_health_report()
  print(json.dumps(asdict(health_report_som), indent=2))


if __name__ == "__main__":
  entrypoint()
