from composition.infrastructure_instances import (DEPLOYMENT_ENVIRONMENT_STR, account_repository, blog_post_repository,
                                                  config_parser, cpu, database, disk, environment, logger, memory,
                                                  typicode_client)
from interfaces.rest.types.infrastructure_collection import InfrastructureCollection
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.repository_collection import RepositoryCollection


def startup(app: ProjectnameFastAPI) -> None:
  logger.debug(f"Using deployment environment: {DEPLOYMENT_ENVIRONMENT_STR}")
  infra = InfrastructureCollection(
    config_parser=config_parser,
    cpu=cpu,
    database=database,
    disk=disk,
    environment=environment,
    logger=logger,
    memory=memory,
    typicode_client=typicode_client
  )
  repos = RepositoryCollection(
    account=account_repository,
    blog_post=blog_post_repository
  )
  app.state.infra = infra
  app.state.repos = repos
