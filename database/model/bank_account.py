

from sqlalchemy import Column, Integer, String, Float

from database.handler import Base


class BankAccount(Base):
    __tablename__ = "bank_account"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    name = Column(String)
    bank_name = Column(String)
    remain = Column(Integer)
    cart_number = Column(String)
    account_number = Column(String)
    description = Column(String)

    def __init__(self, chat_id, bank_name, remain, cart_number):
        self.chat_id = chat_id
        self.bank_name = bank_name
        self.remain = remain
        self.cart_number = cart_number