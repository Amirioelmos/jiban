from database.handler import session
from utils.common import jiban_logger
from database.model.cash_account import CashAccount


def add_cash_account(chat_id, name, remain):
    try:
        ca = CashAccount(chat_id=chat_id, name=name, remain=remain)
        session.add(ca)
        session.commit()
        jiban_logger.info("Add new cash account {}, {}, {}".format(chat_id, name, remain))
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to add new cash account {}, {}, {}".format(chat_id, name, remain))
