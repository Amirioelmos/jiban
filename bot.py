from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, ConversationHandler

from constants.button import BotButton
from constants.messages import BotMessage
from database.logic.user import is_user, add_user
from utils.common import jiban_logger, _get_chat_id
from utils.config import JibanConfig

updater = Updater(token=JibanConfig.bot_token,
                  base_url=JibanConfig.base_url)
dp = updater.dispatcher


def start(bot, update):
    chat_id = _get_chat_id(update)
    is_valid_user = is_user(chat_id)
    if not is_valid_user:
        reply_keyboard = [[
            BotButton.new_cost,
            BotButton.new_account,
            BotButton.account_list,
            BotButton.financial_report,
            BotButton.financial_budgeting,
        ]]
        general_text = BotMessage.starter_message
    else:
        # add_user(chat_id)
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

    update.message.reply_text('Help!')
    return ConversationHandler.END


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    return ConversationHandler.END



def error(bot, update):
    """Log Errors caused by Updates."""
    jiban_logger.warning('Update "%s" caused error "%s"', update, update.message)


