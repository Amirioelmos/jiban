


from sqlalchemy import Column, Integer, String, Float

from database.handler import Base


class CashAccount(Base):
    __tablename__ = "cash_account"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    name = Column(String)
    remain = Column(Integer)
    description = Column(String)

    def __init__(self, chat_id, name, remain):
        self.chat_id = chat_id
        self.name = name
        self.remain = remain