from fastapi import FastAPI

from composition.infrastructure_instances import (DEPLOYMENT_ENVIRONMENT_STR, account_repository, blog_post_repository,
                                                  config_parser, cpu, database, disk, environment, logger, memory,
                                                  typicode_client)
from composition.webserver.types.infra import Infra
from composition.webserver.types.repo import Repo


def startup(app: FastAPI) -> None:
  logger.debug(f"Using deployment environment: {DEPLOYMENT_ENVIRONMENT_STR}")
  infra = Infra(
    config_parser=config_parser,
    cpu=cpu,
    database=database,
    disk=disk,
    environment=environment,
    logger=logger,
    memory=memory,
    typicode_client=typicode_client
  )
  repo = Repo(
    account=account_repository,
    blog_post=blog_post_repository
  )
  app.state.infra = infra
  app.state.repo = repo
