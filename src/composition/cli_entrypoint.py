from composition.models.app_resources import AppResources
from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from composition.resources import get_resources_dict
from composition.webserver.uvicorn_entrypoint import run_webserver
from interfaces.command_line.core.main import add_default_command, build_args, handle_args_routing


def entrypoint():
  resources = build_resources()
  add_default_command()
  args = build_args()
  handle_args_routing(
    args=args,
    logger=resources.infra.logger,
    config_parser=resources.infra.config_parser,
    cpu=resources.infra.cpu,
    database=resources.infra.database,
    disk=resources.infra.disk,
    environment=resources.infra.environment,
    memory=resources.infra.memory,
    typicode_client=resources.infra.typicode_client,
    run_webserver=run_webserver
  )

def build_resources() -> AppResources:
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


if __name__ == "__main__":
  entrypoint()
