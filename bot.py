from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater

from constants.button import BotButton
from constants.messages import BotMessage
from utils.common import jiban_logger
from utils.config import JibanConfig

updater = Updater(token=JibanConfig.bot_token,
                  base_url=JibanConfig.base_url)
dp = updater.dispatcher


def start(bot, update):
    reply_keyboard = [[BotButton.starter]]
    """Send a message when the command /start is issued."""
    update.message.reply_text(BotMessage.starter_message,
                              reply_markup=
                              ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True))


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update):
    """Log Errors caused by Updates."""
    jiban_logger.warning('Update "%s" caused error "%s"', update, update.message)


