from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler

from bot import start, echo, error
from constants.button import BotButton


def handlers_manager(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #
    #     states={
    #         GENDER: [RegexHandler("^{}$".format(BotButton.starter), get_name)],
    #
    #         PHOTO: [MessageHandler(Filters.photo, photo),
    #                 CommandHandler('skip', skip_photo)],
    #
    #         LOCATION: [MessageHandler(Filters.location, location),
    #                    CommandHandler('skip', skip_location)],
    #
    #         BIO: [MessageHandler(Filters.text, bio)]
    #     },
    #
    #     fallbacks=[CommandHandler('cancel', cancel)]
    # )