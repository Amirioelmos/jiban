from sqlalchemy import Column, Integer, String, Boolean

from database.handler import Base


class User(Base):
    __tablename__ = "users"
    chat_id = Column(Integer, primary_key=True)
    name = Column(String)
    payed = Column(Boolean, default=False)

    def __init__(self, chat_id):
        self.chat_id = chat_id
