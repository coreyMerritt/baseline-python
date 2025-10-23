from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class AccountORM(Base):
  __tablename__ = 'accounts'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True, default=None)
  name: Mapped[str] = mapped_column(String, nullable=False)
  age: Mapped[int] = mapped_column(Integer)
  account_type: Mapped[str] = mapped_column(String)
  timestamp: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=lambda: datetime.now(timezone.utc)
  )
