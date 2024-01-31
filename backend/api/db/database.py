from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


# Initializing the Base Class
class Base(DeclarativeBase):
    pass


# Initializing the extension
db = SQLAlchemy(model_class=Base)
