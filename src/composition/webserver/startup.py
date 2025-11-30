import asyncio

from composition.infrastructure_instances import build_raw_infra
from interfaces.rest.models.infrastructure_collection import InfrastructureCollection
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.models.repository_collection import RepositoryCollection


async def startup(app: ProjectnameFastAPI) -> None:
  raw_infra = await asyncio.to_thread(build_raw_infra)
  infra = InfrastructureCollection(
    config_parser=raw_infra["infra"]["config_parser"],
    cpu=raw_infra["infra"]["cpu"],
    database=raw_infra["infra"]["database"],
    disk=raw_infra["infra"]["disk"],
    environment=raw_infra["infra"]["environment"],
    logger=raw_infra["infra"]["logger"],
    memory=raw_infra["infra"]["memory"],
    typicode_client=raw_infra["infra"]["typicode_client"]
  )
  repos = RepositoryCollection(
    account=raw_infra["repos"]["account"],
    blog_post=raw_infra["repos"]["blog_post"]
  )
  app.state.infra = infra
  app.state.repos = repos
  app.infra = infra
  app.repos = repos
  app.infra.logger.debug(f"Using deployment environment: {raw_infra['vars']['deployment_environment_str']}")
  app.infra.logger.info("Startup successful")
