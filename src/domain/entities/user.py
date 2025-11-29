from uuid import uuid4

from domain.exceptions.validation_err import ValidationErr


class User:
  _uuid: str
  _external_mapping_id: str
  _email_address: str
  _username: str

  def __init__(self, uuid: str | None, external_mapping_id: str, email_address: str, username: str):
    if uuid:
      self.uuid = uuid
    else:
      self.uuid = str(uuid4())
    self.external_mapping_id = external_mapping_id
    self.email_address = email_address
    self.username = username

  @property
  def external_mapping_id(self) -> str:
    return self._external_mapping_id

  @external_mapping_id.setter
  def external_mapping_id(self, external_mapping_id: str) -> None:
    if not isinstance(external_mapping_id, str):
      raise ValidationErr("external_mapping_id", "non-str")
    self._external_mapping_id = external_mapping_id

  @property
  def uuid(self) -> str:
    return self._uuid

  @uuid.setter
  def uuid(self, uuid: str) -> None:
    if not isinstance(uuid, str):
      raise ValidationErr("uuid", "non-str")
    self._uuid = uuid

  @property
  def email_address(self) -> str:
    return self._email_address

  @email_address.setter
  def email_address(self, email_address: str) -> None:
    self._email_address = email_address

  @property
  def username(self) -> str:
    return self._username

  @username.setter
  def username(self, username: str) -> None:
    if not isinstance(username, str):
      raise ValidationErr("username", "non-str")
    self._username = username

  def __eq__(self, other):
    return (
      isinstance(other, User)
      and self.uuid == other.uuid
    )
