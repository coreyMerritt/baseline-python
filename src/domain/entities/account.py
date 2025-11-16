from uuid import uuid4

from domain.enums.account_type import AccountType
from domain.exceptions.validation_err import ValidationErr


class Account:
  _uuid: str
  _name: str
  _age: int
  _account_type: AccountType

  def __init__(self, name: str, age: int, account_type: AccountType, uuid: str | None = None):
    if uuid:
      self._uuid = uuid
    else:
      self._uuid = str(uuid4())
    self._name = name
    self._age = age
    self._account_type = account_type
    self._validate_properties()

  def __eq__(self, other):
    return (
      isinstance(other, Account)
      and self._uuid == other._uuid
    )

  def __str__(self) -> str:
    return (
      f"{self.__class__.__name__}(\n"
      f"  name={self._name}\n"
      f"  age={self._age}\n"
      f"  type={self._account_type.value}\n"
      f"  uuid={self._uuid}\n"
      ")"
    )

  def get_name(self) -> str:
    return self._name

  def get_age(self) -> int:
    return self._age

  def get_account_type(self) -> AccountType:
    return self._account_type

  def get_uuid(self) -> str:
    return self._uuid

  def set_name(self, name: str) -> None:
    self._name = name

  def set_age(self, age: int) -> None:
    self._age = age

  def set_account_type(self, account_type: AccountType) -> None:
    self._account_type = account_type

  def set_uuid(self, uuid: str) -> None:
    self._uuid = uuid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self._name, str), "Name is not String"
      assert len(self._name) > 0, "Name is too short"
      assert len(self._name) < 100, "Name is too long"
      assert isinstance(self._age, int), "Age is not int"
      assert self._age > 0, "Age is too low"
      assert self._age < 100, "Age is too high"
      assert isinstance(self._account_type, AccountType), "Account Type doesn't conform to enum standards"
      assert isinstance(self._uuid, str), "UUID is not String"
    except AssertionError as e:
      raise ValidationErr(str(e)) from e
