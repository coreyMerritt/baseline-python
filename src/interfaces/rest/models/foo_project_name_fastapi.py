from fastapi import FastAPI

from composition.models.app_resources import AppResources


class FooProjectNameFastAPI(FastAPI):
  raw_infra: dict
  resources: AppResources
