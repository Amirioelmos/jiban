from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler

from bot import start, echo, error, get_name, choose_service, take_name, take_cash_name, \
    take_cash_amount, save_cash, help_me, create_account_final, new_account
from constants.button import BotButton


def handlers_manager(dp):
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", echo))
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [RegexHandler("^{}$".format(BotButton.starter), get_name)],
            2: [MessageHandler(Filters.text, take_name)],
            3: [MessageHandler(Filters.text, callback=choose_service, pass_user_data=True)],
            4: [MessageHandler(Filters.text, callback=take_cash_name, pass_user_data=True)],
            6: [MessageHandler(Filters.text, callback=take_cash_amount, pass_user_data=True)],
            7: [MessageHandler(Filters.text, callback=save_cash, pass_user_data=True)],
            8: [MessageHandler(Filters.text, callback=create_account_final, pass_user_data=True)],
            9: [RegexHandler(pattern="^{}$".format(BotButton.new_account), callback=new_account, pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.new_cost), callback=help_me, pass_user_data=True)
                ]
            # PHOTO: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],
            #
            # LOCATION: [MessageHandler(Filters.location, location),
            #            CommandHandler('skip', skip_location)],
            #
            # BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', echo)]
    )
    dp.add_handler(conv_handler)