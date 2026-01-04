from typing import Protocol

from composition.models.app_resources import AppResources


class FooProjectNameState(Protocol):
  resources: AppResources
