from domain.exceptions.validation_err import ValidationErr


class Permission:
  _ulid: str
  _key: str

  def __init__(self, ulid: str, key: str):
    self.ulid = ulid
    self.key = key
    self._validate_properties()

  @property
  def ulid(self) -> str:
    return self._ulid

  @ulid.setter
  def ulid(self, ulid: str) -> None:
    self._ulid = ulid

  @property
  def key(self) -> str:
    return self._key

  @key.setter
  def key(self, key: str) -> None:
    self._key = key

  def __eq__(self, other):
    return isinstance(other, Permission) and self.ulid == other.ulid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.ulid, str), "ulid"
      assert isinstance(self.key, str), "key"
      assert "." in self.key, "key"
    except AssertionError as e:
      raise ValidationErr(attribute_name=str(e)) from e
