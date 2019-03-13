from sqlalchemy import Column, Integer, String

from database.handler import Base


class IncomeAndExpenses(Base):
    __tablename__ = "income_and_expenses"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    type = Column(String)
    amount = Column(Integer)
    description = Column(String)

    def __init__(self, chat_id, name, amount):
        self.chat_id = chat_id
        self.name = name
        self.amount = amount