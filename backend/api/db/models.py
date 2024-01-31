import datetime

from backend.api.db.database import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime


class Token(db.Model):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dn: Mapped[str] = mapped_column(String(250), unique=True)
    token: Mapped[str] = mapped_column(String(150))
    datetime_create = mapped_column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f'<{Token.__name__} {self.dn}>'
