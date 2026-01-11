import ulid as ULID

from domain.exceptions.validation_err import ValidationErr


class Role:
  _ulid: str | None
  _name: str

  def __init__(self, ulid: str | None, name: str):
    self.ulid = str(ULID.new())
    if ulid:
      self.ulid = ulid
    self.name = name
    self._validate_properties()

  @property
  def ulid(self) -> str | None:
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

  def __eq__(self, other):
    return isinstance(other, Role) and self.ulid == other.ulid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.ulid, str), "ulid"
      assert isinstance(self.name, str), "name"
      assert self.name.strip(), "name"
    except AssertionError as e:
      raise ValidationErr(attribute_name=str(e)) from e
