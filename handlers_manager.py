from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler

from bot import *
from constants.button import BotButton


common_handler = RegexHandler(pattern=".*", callback=start)
def handlers_manager(dp):
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", echo))
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            RegexHandler(pattern=".*", callback=start)
        ],

        states={
            1: [RegexHandler("^{}$".format(BotButton.starter), get_name), common_handler],
            2: [
                MessageHandler(Filters.text, take_name), common_handler],
            3: [
                MessageHandler(Filters.text, callback=choose_service, pass_user_data=True),
                common_handler
                ],
            4: [
                MessageHandler(Filters.text, callback=take_cash_name, pass_user_data=True),
                common_handler
                ],
            6: [
                MessageHandler(Filters.text, callback=take_cash_amount, pass_user_data=True),
                common_handler
                ],
            5: [
                MessageHandler(Filters.text, callback=take_bank_name_for_account, pass_user_data=True),
                common_handler
                ],

            7: [
                MessageHandler(Filters.text, callback=save_cash_account, pass_user_data=True),
                common_handler
            ],
            8: [
                MessageHandler(Filters.text, callback=create_account_final, pass_user_data=True),
                common_handler
                ],
            9: [
                RegexHandler(pattern="^{}$".format(BotButton.new_account), callback=new_account, pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.new_cost), callback=new_income_and_expenses, pass_user_data=True),
                common_handler

                ],
            10: [
                MessageHandler(Filters.text, callback=take_remain_of_bank_account, pass_user_data=True),
                common_handler
                 ],
            11: [
                MessageHandler(Filters.text, callback=take_cart_number_of_bank_account, pass_user_data=True),
                common_handler
                 ],


            12: [
                RegexHandler(pattern="^{}$".format(BotButton.yes_add),
                             callback=save_bank_account,
                             pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.no_change_it),
                             callback=take_bank_name_for_account,
                             pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.add_account_number),
                             callback=get_account_number_of_bank_account,
                             pass_user_data=True),
                common_handler
                ],
            13: [
                MessageHandler(Filters.text, callback=take_account_number_of_bank_account, pass_user_data=True),
                common_handler
                ],
            14: [
                MessageHandler(Filters.text, callback=pay_full_bot, pass_user_data=True),
                common_handler
                ],
            15: [
                MessageHandler(Filters.successful_payment, callback=pay_full_done, pass_user_data=True),
                common_handler
            ],
            16: [
                RegexHandler(pattern="^{}$".format(BotButton.cost),
                             callback=new_cost,
                             pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.receive),
                             callback=new_receive,
                             pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.p2p),
                             callback=get_account_number_of_bank_account,
                             pass_user_data=True),
                RegexHandler(pattern="^{}$".format(BotButton.auto_understand_transactions),
                             callback=new_auto_understand_transactions,
                             pass_user_data=True),
                common_handler
            ],
            17: [
                MessageHandler(Filters.text, callback=take_cost_type, pass_user_data=True),
                common_handler
            ],
            18: [
                MessageHandler(Filters.text, callback=take_cost_amount, pass_user_data=True),
                common_handler
            ],
            19: [
                MessageHandler(Filters.text, callback=take_cost_date, pass_user_data=True),
                common_handler
            ],
            20: [
                MessageHandler(Filters.text, callback=take_cost_account, pass_user_data=True),
                common_handler
            ],

            21: [
                MessageHandler(Filters.text, callback=take_receive_type, pass_user_data=True),
                common_handler
            ],
            22: [
                MessageHandler(Filters.text, callback=take_receive_amount, pass_user_data=True),
                common_handler
            ],
            23: [
                MessageHandler(Filters.text, callback=take_receive_date, pass_user_data=True),
                common_handler
            ],
            24: [
                MessageHandler(Filters.text, callback=take_receive_account, pass_user_data=True),
                common_handler
            ],
            # PHOTO: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],
            #
            # LOCATION: [MessageHandler(Filters.location, location),
            #            CommandHandler('skip', skip_location)],
            #
            # BIO: [MessageHandler(Filters.text, bio)]
            0: [RegexHandler(".*", start)],

        },

        fallbacks=[CommandHandler('cancel', echo)]
    )
    dp.add_handler(conv_handler)