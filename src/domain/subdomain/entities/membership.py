from datetime import datetime

from domain.enums.membership_status import MembershipStatus
from domain.exceptions.validation_err import ValidationErr


class Membership:
  _ulid: str
  _user_ulid: str
  _account_ulid: str
  _role_ulid: str
  _status: MembershipStatus
  _joined_at: datetime
  _removed_at: datetime | None

  def __init__(
    self,
    ulid: str,
    user_ulid: str,
    account_ulid: str,
    role_ulid: str,
    status: MembershipStatus,
    joined_at: datetime,
    removed_at: datetime | None = None,
  ):
    self.ulid = ulid
    self.user_ulid = user_ulid
    self.account_ulid = account_ulid
    self.role_ulid = role_ulid
    self.status = status
    self.joined_at = joined_at
    self.removed_at = removed_at
    self._validate_properties()

  @property
  def ulid(self) -> str:
    return self._ulid

  @ulid.setter
  def ulid(self, ulid: str) -> None:
    self._ulid = ulid

  @property
  def user_ulid(self) -> str:
    return self._user_ulid

  @user_ulid.setter
  def user_ulid(self, user_ulid: str) -> None:
    self._user_ulid = user_ulid

  @property
  def account_ulid(self) -> str:
    return self._account_ulid

  @account_ulid.setter
  def account_ulid(self, account_ulid: str) -> None:
    self._account_ulid = account_ulid

  @property
  def role_ulid(self) -> str:
    return self._role_ulid

  @role_ulid.setter
  def role_ulid(self, role_ulid: str) -> None:
    self._role_ulid = role_ulid

  @property
  def status(self) -> MembershipStatus:
    return self._status

  @status.setter
  def status(self, status: MembershipStatus) -> None:
    self._status = status

  @property
  def joined_at(self) -> datetime:
    return self._joined_at

  @joined_at.setter
  def joined_at(self, joined_at: datetime) -> None:
    self._joined_at = joined_at

  @property
  def removed_at(self) -> datetime | None:
    return self._removed_at

  @removed_at.setter
  def removed_at(self, removed_at: datetime | None) -> None:
    self._removed_at = removed_at

  def __eq__(self, other):
    return isinstance(other, Membership) and self.ulid == other.ulid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.ulid, str), "ulid"
      assert isinstance(self.user_ulid, str), "user_ulid"
      assert isinstance(self.account_ulid, str), "account_ulid"
      assert isinstance(self.role_ulid, str), "role_ulid"
      assert isinstance(self.status, MembershipStatus), "status"
      assert isinstance(self.joined_at, datetime), "joined_at"
      assert (
        self.removed_at is None
        or isinstance(self.removed_at, datetime)
      ), "removed_at"
    except AssertionError as e:
      raise ValidationErr(attribute_name=str(e)) from e
