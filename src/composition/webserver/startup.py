import asyncio

from composition.infrastructure_instances import get_instances_dict
from interfaces.rest.models.infrastructure_collection import InfrastructureCollection
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.models.repository_collection import RepositoryCollection


async def startup(app: ProjectnameFastAPI) -> None:
  instances = await _get_instances(app)
  infra = InfrastructureCollection(
    config_parser=instances["infra"]["config_parser"],
    cpu=instances["infra"]["cpu"],
    database=instances["infra"]["database"],
    disk=instances["infra"]["disk"],
    environment=instances["infra"]["environment"],
    logger=instances["infra"]["logger"],
    memory=instances["infra"]["memory"],
    typicode_client=instances["infra"]["typicode_client"]
  )
  repos = RepositoryCollection(
    account=instances["repos"]["account"],
    blog_post=instances["repos"]["blog_post"],
    membership=instances["repos"]["membership"],
    role=instances["repos"]["role"],
    user=instances["repos"]["user"]
  )
  app.state.infra = infra
  app.state.repos = repos
  app.infra = infra
  app.repos = repos
  app.infra.logger.info("Startup successful")

async def _get_instances(app: ProjectnameFastAPI) -> dict:
  stop_event = app.state.stop_event
  blocking_task = asyncio.create_task(asyncio.to_thread(get_instances_dict))
  signal_task = asyncio.create_task(stop_event.wait())
  done, _ = await asyncio.wait(
    {blocking_task, signal_task},
    return_when=asyncio.FIRST_COMPLETED
  )
  if signal_task in done:
    blocking_task.cancel()
    raise KeyboardInterrupt("Startup interrupted by user.")
  instances = blocking_task.result()
  return instances
