from datetime import UTC, datetime

import ulid as ULID

from domain.enums.account_status import AccountStatus
from domain.exceptions.validation_err import ValidationErr


class Account:
  _ulid: str
  _name: str
  _status: AccountStatus
  _created_at: datetime
  _suspended_at: datetime | None
  _deleted_at: datetime | None

  def __init__(
    self,
    name: str,
    ulid: str | None,
    status: AccountStatus | None,
    created_at: datetime | None,
    suspended_at: datetime | None,
    deleted_at: datetime | None
  ):
    self.name = name
    self.ulid = str(ULID.new())
    if ulid:
      self.ulid = ulid
    self.status = AccountStatus.ACTIVE
    if status:
      self.status = status
    self.created_at = datetime.now(tz=UTC)
    if created_at:
      self.created_at = created_at
    self.suspended_at = suspended_at
    self.deleted_at = deleted_at
    self._validate_properties()

  @property
  def ulid(self) -> str:
    return self._ulid

  @ulid.setter
  def ulid(self, ulid: str) -> None:
    self._ulid = ulid

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    self._name = name

  @property
  def status(self) -> AccountStatus:
    return self._status

  @status.setter
  def status(self, status: AccountStatus) -> None:
    if status == AccountStatus.SUSPENDED and not self._status == AccountStatus.SUSPENDED:
      self._suspended_at = datetime.now(UTC)
    if status == AccountStatus.DELETED and not self._status == AccountStatus.DELETED:
      self._deleted_at = datetime.now(UTC)
    self._status = status

  @property
  def created_at(self) -> datetime:
    return self._created_at

  @created_at.setter
  def created_at(self, created_at: datetime) -> None:
    self._created_at = created_at

  @property
  def suspended_at(self) -> datetime | None:
    return self._suspended_at

  @suspended_at.setter
  def suspended_at(self, suspended_at: datetime | None) -> None:
    self._suspended_at = suspended_at

  @property
  def deleted_at(self) -> datetime | None:
    return self._deleted_at

  @deleted_at.setter
  def deleted_at(self, deleted_at: datetime | None) -> None:
    self._deleted_at = deleted_at

  def __eq__(self, other):
    return isinstance(other, Account) and self.ulid == other.ulid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.ulid, str), "ulid"
      assert self.ulid.strip(), "ulid"
      assert isinstance(self.name, str), "name"
      assert self.name.strip(), "name"
      assert isinstance(self.status, AccountStatus), "status"
      assert isinstance(self.created_at, datetime), "created_at"
      assert (
        self.suspended_at is None
        or isinstance(self.suspended_at, datetime)
      ), "suspended_at"
      assert (
        self.deleted_at is None
        or isinstance(self.deleted_at, datetime)
      ), "deleted_at"
    except AssertionError as e:
      raise ValidationErr(attribute_name=str(e)) from e
