import datetime

from backend.api.db.database import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime


class TokenModel(db.Model):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dn: Mapped[str] = mapped_column(String(250), unique=True)
    uid: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(50))
    token: Mapped[str] = mapped_column(String(150))
    datetime_create = mapped_column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f'<{TokenModel.__name__} {self.dn}>'
