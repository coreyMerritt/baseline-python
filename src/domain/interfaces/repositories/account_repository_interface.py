from typing import Protocol

from domain.entities.account import Account


class AccountRepositoryInterface(Protocol):
  def get(self, uuid: str) -> Account: ...
  def insert(self, account: Account) -> Account: ...
