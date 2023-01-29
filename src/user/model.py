import datetime
# from src.utils.update import update_fields
from src.utils.defaultcol import DefaultColumns
from src.database_files.database import Base
from sqlalchemy import String, Boolean, Column



class User(DefaultColumns, Base):
    __tablename__ = "user"
    name = Column(String(255))
    password = Column(String(255))
    email = Column(String(255), unique = True)

    def update_fields(self, update: dict):
            for key, value in update.items():
                if value:
                    setattr(self, key, value)
