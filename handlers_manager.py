from telegram.ext import CommandHandler, MessageHandler, Filters

from jiban_main import start, echo, error


def handlers_manager(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)