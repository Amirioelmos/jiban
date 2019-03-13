import persian

from database.logic.cash_account import add_cash_account
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, ConversationHandler

from constants.button import BotButton
from constants.messages import BotMessage
from database.logic.user import is_user, add_user, update_user, get_user_name
from utils.common import jiban_logger, _get_chat_id, _get_message, UserData, _formatter
from utils.config import JibanConfig

updater = Updater(token=JibanConfig.bot_token,
                  base_url=JibanConfig.base_url)
dp = updater.dispatcher


def start(bot, update):
    chat_id = _get_chat_id(update)
    is_valid_user = is_user(chat_id)
    if is_valid_user:
        reply_keyboard = [[
            BotButton.new_cost,
            BotButton.new_account,
            BotButton.account_list,
            BotButton.financial_report,
            BotButton.financial_budgeting,
        ]]
        general_text = BotMessage.starter_message
        update.message.reply_text(general_text,
                                  reply_markup=
                                  ReplyKeyboardMarkup(
                                      reply_keyboard,
                                      one_time_keyboard=True))
        return 9
    else:
        add_user(chat_id)
        reply_keyboard = [[BotButton.starter]]
        general_text = BotMessage.greeting_message
        update.message.reply_text(general_text,
                                  reply_markup=
                                  ReplyKeyboardMarkup(
                                      reply_keyboard,
                                      one_time_keyboard=True))
        return 1


def get_name(bot, update):
    chat_id = _get_chat_id(update)
    text = BotMessage.enter_name
    bot.send_message(chat_id=chat_id, text=text)
    return 2


def take_name(bot, update):
    chat_id = _get_chat_id(update)
    name = _get_message(update)
    update_user(chat_id, name)
    reply_keyboard = [[BotButton.account, BotButton.cash]]
    text = BotMessage.choose_service.format(name=name)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=
        ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True))
    return 3


def new_account(bot, update, user_data):
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    reply_keyboard = [[BotButton.account, BotButton.cash]]
    text = BotMessage.choose_service.format(name=name)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=
        ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True))
    return 3


def choose_service(bot, update, user_data):
    jiban_logger.info("\n\nchoose_service\n\n")
    message = _get_message(update)
    reply_keyboard = [[BotButton.main_menu]]
    if message == BotButton.account:
        user_data[UserData.account_type] = message
        text = BotMessage.choose_bank_of_account
        bot.send_message(
            chat_id=_get_chat_id(update),
            text=text,
            reply_markup=
            ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True))
        return 5
    if message == BotButton.cash:
        user_data[UserData.account_type] = message
        text = BotMessage.choose_name_for_cash
        bot.send_message(
            chat_id=_get_chat_id(update),
            text=text,
            reply_markup=
            ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True))
        return 4


def take_cash_name(bot, update, user_data):
    jiban_logger.info("\n\ntake_cash_name\n\n")
    message = _get_message(update)
    if message == BotButton.main_menu:
        return start(bot, update)
    user_data[UserData.cash_name] = message
    text = BotMessage.enter_amount_of_cash.format(name=message)
    bot.send_message(
        chat_id=_get_chat_id(update),
        text=text)
    return 6


def take_cash_amount(bot, update, user_data):
    jiban_logger.info("\n\ntake_cash_amount\n\n")
    name = user_data[UserData.cash_name]
    amount = _get_message(update)
    user_data[UserData.cash_amount] = amount
    amount = _formatter(int(amount))
    text = BotMessage.accept_to_add_your_accounts.format(name=name, amount=amount)
    reply_keyboard = [[BotButton.yes_add, BotButton.no_change_it]]
    bot.send_message(
        chat_id=_get_chat_id(update),
        text=text,
        reply_markup=
        ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True))
    return 7


def save_cash(bot, update, user_data):
    name = user_data[UserData.cash_name]
    amount = user_data[UserData.cash_amount]
    chat_id = _get_chat_id(update)
    add_cash_account(chat_id, name, amount)
    text = BotMessage.new_cash_account_done.format(name=name)
    reply_keyboard = [[BotButton.main_menu, BotButton.new_account]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard,
                        one_time_keyboard=True))
    return 8


def create_account_final(bot, update, user_data):
    message = _get_message(update)
    if message == BotButton.main_menu:
        return start(bot, update)
    if message == BotButton.new_account:
        return new_account(bot, update, user_data)

# def take_cash_account_text(bot, update, user_data):
#     message = _get_message(update)
#     user_data['cash_account_name'] = message
#     text = BotMessage.enter_amount_of_cash
#     bot.send_message(
#         chat_id=_get_chat_id(update),
#         text=text)
#     return take_cash_amount(bot, update, user_data)
#
#
# def take_cash_amount(bot, update, user_data):
#     update.message.reply_text('Help!')


def help_me(bot, update, user_data):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    return ConversationHandler.END



def error(bot, update):
    """Log Errors caused by Updates."""
    jiban_logger.warning('Update "%s" caused error "%s"', update, update.message)


