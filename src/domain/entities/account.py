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
      self.uuid = uuid
    else:
      self.uuid = str(uuid4())
    self.name = name
    self.age = age
    self.account_type = account_type
    self._validate_properties()

  @property
  def uuid(self) -> str:
    return self._uuid

  @uuid.setter
  def uuid(self, uuid: str) -> None:
    self._uuid = uuid

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    self._name = name

  @property
  def age(self) -> int:
    return self._age

  @age.setter
  def age(self, age: int) -> None:
    self._age = age

  @property
  def account_type(self) -> AccountType:
    return self._account_type

  @account_type.setter
  def account_type(self, account_type: AccountType) -> None:
    self._account_type = account_type

  def __eq__(self, other):
    return (
      isinstance(other, Account)
      and self._uuid == other._uuid
    )

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self._name, str), "name"
      assert len(self._name) >= 1, "name"
      assert len(self._name) <= 99, "name"
      assert isinstance(self._age, int), "age"
      assert self._age >= 1, "age"
      assert self._age <= 99, "age"
      assert isinstance(self._account_type, AccountType), "account_type"
      assert isinstance(self._uuid, str), "uuid"
    except AssertionError as e:
      raise ValidationErr(
        attribute_name=str(e)
      ) from e
