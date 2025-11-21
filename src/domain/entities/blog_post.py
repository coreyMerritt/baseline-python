from domain.exceptions.validation_err import ValidationErr


class BlogPost:
  _user_id: int
  _id: int
  _title: str
  _body: str

  def __init__(self, user_id: int, id_: int, title: str, body: str):
    self.user_id = user_id
    self.id = id_
    self.title = title
    self.body = body
    self._validate_properties()

  @property
  def user_id(self) -> int:
    return self._user_id

  @user_id.setter
  def user_id(self, user_id: int) -> None:
    self._user_id = user_id

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, id_: int) -> None:
    self._id = id_

  @property
  def title(self) -> str:
    return self._title

  @title.setter
  def title(self, title: str) -> None:
    self._title = title

  @property
  def body(self) -> str:
    return self._body

  @body.setter
  def body(self, body: str) -> None:
    self._body = body

  def __eq__(self, other):
    return (
      isinstance(other, BlogPost)
      and self.id == other.id
    )

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.user_id, int), "user_id"
      assert self.user_id >= 1, "user_id"
      assert self.user_id <= 10, "user_id"
      assert isinstance(self.id, int), "id"
      assert self.id >= 1, "id"
      assert self.id <= 100, "id"
      assert isinstance(self.title, str), "title"
      assert isinstance(self.body, str), "body"
    except AssertionError as e:
      raise ValidationErr(
        attribute_name=str(e)
      ) from e
