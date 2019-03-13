from database.handler import session
from database.model.cash_account import CashAccount
from utils.common import jiban_logger


def add_cash_account(chat_id, name, amount):
    try:
        ca = CashAccount(chat_id=chat_id, name=name, amount=amount)
        session.add(ca)
        session.commit()
        jiban_logger.info("Add new cash account {}, {}, {}".format(chat_id, name, amount))
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to add new cash account {}, {}, {}".format(chat_id, name, amount))
