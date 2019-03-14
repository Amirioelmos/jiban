
from database.handler import session
from database.model.bank_account import BankAccount
from database.model.cash_account import CashAccount
from database.model.income_and_expenses import IncomeAndExpenses, IEText
from utils.common import jiban_logger


def add_income_and_expenses(chat_id, account, kind, type, amount):
    try:
        account_type = get_account_type(account)
        ie = IncomeAndExpenses(chat_id=chat_id,
                               account_id=account.id,
                               account_type=account_type,
                               amount=int(amount),
                               type=type,
                               kind=kind)
        if kind == IEText.deposit:
            deposit(chat_id, account.id, account_type, amount)
        session.add(ie)
        session.commit()
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to add IncomeAndExpenses : \n for {}".format(e))


def deposit(chat_id, account_id, account_type, amount):
    try:
        if account_type == IEText.bank_account:
            account = session.query(BankAccount).filter(
                BankAccount.chat_id == chat_id).filter(
                BankAccount.id == account_id
            ).first()
            account.remain -= int(amount)
        else:
            account = session.query(CashAccount).filter(
                CashAccount.chat_id == chat_id).filter(
                CashAccount.id == account_id
            ).first()
            account.remain -= int(amount)
        session.commit()
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to deposit, chat_id : {}, id : {}, type : {}, amount : {}\n for {}".format(
            chat_id, account_id, account_type, amount, e
        ))


def get_account_type(account):
    if isinstance(account, BankAccount):
        return IEText.bank_account
    else:
        return IEText.cash_account
