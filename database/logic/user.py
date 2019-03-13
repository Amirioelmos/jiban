from sqlalchemy import func

from database.handler import session
from database.model.bank_account import BankAccount
from database.model.cash_account import CashAccount
from database.model.user import User
from utils.common import jiban_logger


def add_user(chat_id):
    try:
        user = User(chat_id)
        session.add(user)
        session.commit()
        jiban_logger.info("New User Added. : {}".format(chat_id))
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to Add new user : {}".format(e))


def is_user(chat_id):
    is_user_flag = False
    try:
        user = session.query(User).filter(User.chat_id == chat_id).first()
        if user:
            jiban_logger.info("User found : {}".format(user.chat_id))
            is_user_flag = True
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to load user : {}, {}".format(chat_id, e))
    return is_user_flag


def update_user(chat_id, name):
    try:
        user = session.query(User).filter(User.chat_id == chat_id).first()
        user.name = name
        session.commit()
        jiban_logger.info("Update user : {}, name: {}".format(chat_id, name))
    except Exception as e:
        session.rollback()
        jiban_logger.info("Update user fail, {}, by {}".format(chat_id, e))


def get_user_name(chat_id):
    try:
        name = session.query(User.name).filter(User.chat_id == chat_id).first()
        if name:
            return name[0]
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to load name of : {}".format(chat_id))


def check_payed_user(chat_id):
    try:
        user = session.query(User).filter(User.chat_id == chat_id).first()
        if user.payed:
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to check user payed: {}\n for : {}".format(chat_id, e))
        return True


def number_of_account(chat_id):
    try:
        number_of_cash_account = session.query(func.count(CashAccount.chat_id)).filter(CashAccount.chat_id == chat_id).scalar()
        number_of_bank_account = session.query(func.count(BankAccount.chat_id)).filter(BankAccount.chat_id == chat_id).scalar()
        jiban_logger.info("\n number_of_cash_account : {}\n number_of_bank_account : {}".format(number_of_cash_account, number_of_bank_account))
        return number_of_bank_account + number_of_cash_account
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to load number_of_account, for : {}".format(e))


def set_user_payed(chat_id):
    try:
        user = session.query(User).filter(User.chat_id == chat_id).first()
        user.payed = True
        session.commit()
        jiban_logger.info("User payed : {}".format(chat_id))
    except Exception as e:
        session.rollback()
        jiban_logger.info("Fail to set user payed : {}\n for {}".format(chat_id, e))


def get_accounts_of_user(chat_id):
    account_list = []
    try:
        bank_accounts = session.query(BankAccount).filter(BankAccount.chat_id == chat_id).all()
        cash_accounts = session.query(CashAccount).filter(CashAccount.chat_id == chat_id).all()
        if bank_accounts:
            account_list += bank_accounts
        if cash_accounts:
            account_list += cash_accounts
        return account_list
    except Exception as e:
        session.rollback()
        jiban_logger.info("fail to load all accounts : {}".format(e))
        return account_list