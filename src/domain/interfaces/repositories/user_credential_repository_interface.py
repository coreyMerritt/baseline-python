from typing import Protocol

from infrastructure.auth.models.user_credential import UserCredential


class UserCredentialRepositoryInterface(Protocol):
  def get(self, ulid: str) -> UserCredential: ...
