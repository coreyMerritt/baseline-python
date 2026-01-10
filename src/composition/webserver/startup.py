import asyncio

from composition.models.app_resources import AppResources
from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from composition.resources import get_resources_dict
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI


async def startup(app: FooProjectNameFastAPI) -> None:
  resources_dict = await _get_resources_dict(app)
  infra = InfrastructureCollection(
    authenticator=resources_dict["infra"]["authenticator"],
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
  app.state.resources = resources
  app.resources = resources
  app.resources.infra.logger.info("Startup successful")

async def _get_resources_dict(app: FooProjectNameFastAPI) -> dict:
  stop_event = app.state.stop_event
  blocking_task = asyncio.create_task(asyncio.to_thread(get_resources_dict))
  signal_task = asyncio.create_task(stop_event.wait())
  done, _ = await asyncio.wait(
    {blocking_task, signal_task},
    return_when=asyncio.FIRST_COMPLETED
  )
  if signal_task in done:
    blocking_task.cancel()
    raise KeyboardInterrupt("Startup interrupted by user.")
  resources = blocking_task.result()
  return resources
