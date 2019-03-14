import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database.handler import Base


class IncomeAndExpenses(Base):
    __tablename__ = "income_and_expenses"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    account_type = Column(String)
    chat_id = Column(Integer)
    type = Column(String) # category example family
    amount = Column(Integer)
    description = Column(String)
    date = Column(DateTime)
    kind = Column(String)  # cost, receive

    def __init__(self, chat_id, account_id, account_type, type, kind ,amount):
        self.chat_id = chat_id
        self.type = type
        self.kind = kind
        self.account_id = account_id
        self.account_type = account_type
        self.amount = amount
        self.date = datetime.datetime.now()


class IEText:
    cash_account = "cash_account"
    bank_account = "bank_account"
    deposit = "deposit"
    withdraw = "withdraw"
    pocket_to_pocket = "pocket_to_pocket"
