from database.handler import session
from database.model.bank_account import BankAccount
from utils.common import jiban_logger


def add_bank_account(chat_id, bank_name, remain, cart_number):
    try:
        ba = BankAccount(chat_id=chat_id, bank_name=bank_name, remain=remain, cart_number=cart_number)
        session.add(ba)
        session.commit()
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to add new bank account  : {},  {},  {}\n for : {}".format(chat_id, bank_name, remain, e))


def update_bank_account(chat_id, card_number, key, value):
    try:
        session.query(BankAccount).filter(
            BankAccount.chat_id == chat_id
        ).filter(BankAccount.cart_number == card_number).update({key: value})
        session.commit()
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to update BankAccount: {}, {}\n for : {}".format(chat_id, card_number, e))
