from database.handler import session
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
        jiban_logger.info("User found : {}".format(user.chat_id))
        if user:
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
