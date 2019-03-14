import json

import persian

from database.logic.bank_account import add_bank_account, update_bank_account
from database.logic.cash_account import add_cash_account
from database.logic.income_and_expenses import add_income_and_expenses
from database.model.bank_account import BankAccount
from database.model.income_and_expenses import IEText
from telegram import ReplyKeyboardMarkup, LabeledPrice
from telegram.ext import Updater, ConversationHandler

from constants.button import BotButton
from constants.messages import BotMessage, MiniText
from database.logic.user import is_user, add_user, update_user, get_user_name, check_payed_user, number_of_account, \
    set_user_payed, get_accounts_of_user
from utils.common import jiban_logger, _get_chat_id, _get_message, UserData, _formatter
from utils.config import JibanConfig

updater = Updater(token=JibanConfig.bot_token,
                  base_url=JibanConfig.base_url)
dp = updater.dispatcher


def start(bot, update, user_data):
    message = _get_message(update)
    if str(message).__contains__(MiniText.bank_melli):
        user_data[UserData.sapta_message] = message
        return auto_understand_sapta(bot, update, user_data)
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


def get_name(bot, update, user_data):
    chat_id = _get_chat_id(update)
    starter_checker(bot, update, user_data)
    reply_keyboard = [[BotButton.main_menu]]
    text = BotMessage.enter_name
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=
                     ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 2


def take_name(bot, update, user_data):
    chat_id = _get_chat_id(update)
    starter_checker(bot, update, user_data)
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
    starter_checker(bot, update, user_data)
    reply_keyboard = [[BotButton.account, BotButton.cash]]
    is_user_payed = check_payed_user(chat_id)
    number_of_account_for_user = number_of_account(chat_id)
    if number_of_account_for_user < 3:
        text = BotMessage.choose_service.format(name=name)
        bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=
            ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True))
        return 3
    else:
        if is_user_payed:
            text = BotMessage.choose_service.format(name=name)
            bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True))
            return 3
        else:
            user_name = get_user_name(chat_id)
            text = BotMessage.please_pay_for_continue.format(name=user_name)
            reply_keyboard = [[BotButton.pay, BotButton.main_menu]]
            bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True))
            return 14


def pay_full_bot(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    bot.send_invoice(chat_id=chat_id,
                     title=BotMessage.invoice_text,
                     description=BotMessage.invoice_description,
                     payload="payload",
                     provider_token=JibanConfig.cart_number,
                     start_parameter="",
                     currency="IRR",
                     prices=
                     [LabeledPrice(
                         BotMessage.invoice_labale,
                         JibanConfig.pay_amount
                     )])
    return 15


def pay_full_done(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    successful_payment = update.message.successful_payment
    jiban_logger.info("SuccessfulPayment with payload: %s", successful_payment.invoice_payload)
    invoice_payload = json.loads(successful_payment.invoice_payload)
    set_user_payed(chat_id)
    text = BotMessage.thanks_for_payed
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=
        ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True))

    return 0


def choose_service(bot, update, user_data):
    starter_checker(bot, update, user_data)
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
    starter_checker(bot, update, user_data)
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
    starter_checker(bot, update, user_data)
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


def save_cash_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
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
    starter_checker(bot, update, user_data)
    message = _get_message(update)
    if message == BotButton.main_menu:
        return start(bot, update, user_data)
    if message == BotButton.new_account:
        return new_account(bot, update, user_data)


def take_bank_name_for_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    user_data[UserData.bank_name] = message
    text = BotMessage.enter_remain_of_bank_account
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 10


def take_remain_of_bank_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    message = _get_message(update)
    chat_id = _get_chat_id(update)
    user_data[UserData.bank_account_remain] = message
    text = BotMessage.enter_cart_number_of_bank_account
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 11


def take_cart_number_of_bank_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    message = _get_message(update)
    chat_id = _get_chat_id(update)

    user_data[UserData.back_account_cart_number] = message
    bank_name = user_data[UserData.bank_name]
    remain = user_data[UserData.bank_account_remain]
    remain = _formatter(int(remain))
    message = persian.convert_en_numbers(message)
    text = BotMessage.accept_to_add_bank_account.format(bank_name=bank_name,
                                                        remain=remain,
                                                        cart_number=message)
    reply_keyboard = [[
        BotButton.yes_add,
        BotButton.add_account_number,
        BotButton.add_account_name,
        BotButton.no_change_it,
    ]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 12


def save_bank_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    message = _get_message(update)
    chat_id = _get_chat_id(update)
    bank_name = user_data[UserData.bank_name]
    remain = user_data[UserData.bank_account_remain]
    cart_number = user_data[UserData.back_account_cart_number]
    add_bank_account(chat_id, bank_name, remain, cart_number)
    account_number = None
    try:
        account_number = user_data[UserData.back_account_account_number]
    except Exception as e:
        pass
    if account_number:
        update_bank_account(chat_id, cart_number, "account_number", account_number)
    text = BotMessage.new_bank_account_done.format(bank_name=bank_name)
    reply_keyboard = [[BotButton.main_menu, BotButton.new_account]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 8


def get_account_number_of_bank_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    text = BotMessage.enter_account_number
    chat_id = _get_chat_id(update)
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 13


def take_account_number_of_bank_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    user_data[UserData.back_account_account_number] = message
    reply_keyboard = [[
        BotButton.yes_add,
        BotButton.add_account_name,
        BotButton.no_change_it,
    ]]
    bank_name = user_data[UserData.bank_name]
    cart_number = user_data[UserData.back_account_cart_number]
    remain = user_data[UserData.bank_account_remain]
    text = BotMessage.new_bank_account_done_by_account_number.format(
        bank_name=bank_name,
        cart_number=cart_number,
        remain=remain,
        account_number=message)
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 12


def new_income_and_expenses(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    text = BotMessage.new_cost.format(name=name)
    reply_keyboard = [[
        BotButton.cost,
        BotButton.receive,
        BotButton.p2p,
        BotButton.auto_understand_transactions,
    ]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 16


def new_cost(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    text = BotMessage.choose_cost_category
    reply_keyboard = [[
        BotButton.edu,
        BotButton.fun,
        BotButton.family,
        BotButton.charge,
    ]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 17


def take_cost_type(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    reply_keyboard = [[BotButton.main_menu]]
    user_data[UserData.cost_type] = message
    text = BotMessage.enter_amount_of_cost
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=
                     ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 18


def take_cost_amount(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    reply_keyboard = [[BotButton.main_menu]]
    user_data[UserData.cost_amount] = message
    text = BotMessage.enter_date_of_cost
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=
                     ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 19


def take_cost_date(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    user_data[UserData.cost_date] = message
    text = BotMessage.enter_account_of_cost
    all_accounts = get_accounts_of_user(chat_id)
    user_data[UserData.all_accounts] = all_accounts
    account_info = []
    if all_accounts:
        for account in all_accounts:
            if isinstance(account, BankAccount):
                item = str(all_accounts.index(account)) + " " + account.bank_name
            else:
                item = str(all_accounts.index(account)) + " " + MiniText.cash
            account_info.append(item)
    account_info.append(BotButton.main_menu)
    reply_keyboard = [account_info]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 20


def take_cost_account(bot, update, user_data):
    chat_id = _get_chat_id(update)
    starter_checker(bot, update, user_data)
    account_info = _get_message(update).split(" ")
    account_id = account_info[0]
    account = user_data[UserData.all_accounts][int(account_id)]
    name = get_user_name(chat_id)
    if isinstance(account, BankAccount):
        account_name = account.bank_name
    else:
        account_name = MiniText.cash

    user_data[UserData.cost_account] = account.id
    cost_type = user_data[UserData.cost_type]
    amount = user_data[UserData.cost_amount]
    add_income_and_expenses(chat_id=chat_id,
                            account=account,
                            type=cost_type,
                            kind=IEText.deposit,
                            amount=amount)
    text = BotMessage.cost_saved.format(
        name=name,
        cost_type=cost_type,
        amount=_formatter(int(amount)),
        account_name=account_name,
        remain=_formatter(account.remain)
    )
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 0


def new_receive(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    text = BotMessage.choose_cost_category
    reply_keyboard = [[
        BotButton.salary,
        BotButton.sell,
        BotButton.profitable_investment,
        BotButton.gifts_and_rewards,
    ]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 21


def take_receive_type(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    reply_keyboard = [[BotButton.main_menu]]
    user_data[UserData.receive_type] = message
    text = BotMessage.enter_amount_of_receive
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=
                     ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 22


def take_receive_amount(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    reply_keyboard = [[BotButton.main_menu]]
    user_data[UserData.receive_amount] = message
    text = BotMessage.enter_date_of_receive
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=
                     ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 23


def take_receive_date(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    message = _get_message(update)
    user_data[UserData.receive_date] = message
    text = BotMessage.enter_account_of_cost
    all_accounts = get_accounts_of_user(chat_id)
    user_data[UserData.all_accounts] = all_accounts
    account_info = []
    if all_accounts:
        for account in all_accounts:
            if isinstance(account, BankAccount):
                item = str(all_accounts.index(account)) + " " + account.bank_name
            else:
                item = str(all_accounts.index(account)) + " " + MiniText.cash
            account_info.append(item)
    account_info.append(BotButton.main_menu)
    reply_keyboard = [account_info]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 24


def take_receive_account(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    account_info = _get_message(update).split(" ")
    account_id = account_info[0]
    account = user_data[UserData.all_accounts][int(account_id)]
    name = get_user_name(chat_id)
    user_data[UserData.receive_date_account] = account.id
    cost_type = user_data[UserData.receive_type]
    amount = user_data[UserData.receive_amount]
    if isinstance(account, BankAccount):
        account_name = account.bank_name
    else:
        account_name = MiniText.cash
    add_income_and_expenses(chat_id=chat_id,
                            account=account,
                            type=cost_type,
                            kind=IEText.withdraw,
                            amount=amount)
    text = BotMessage.receive_saved.format(
        name=name,
        receive_type=cost_type,
        amount=_formatter(int(amount)),
        account_name=account_name,
        remain=_formatter(account.remain)
    )
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 0


def new_p2p(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    bot.send_message(text="new_p2p {}".format(name), chat_id=chat_id)


def new_auto_understand_transactions(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    reply_keyboard = [[BotButton.main_menu]]
    text = BotMessage.get_me_spata_message
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 25


def auto_understand_sapta(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    if name is None:
        name = MiniText.user
    message = user_data[UserData.sapta_message]
    message_info = str(message).split("\n")
    transaction_type = message_info[1]
    transaction_amount = message_info[2]
    remain = message_info[3]
    account_number = message_info[4]
    date = message_info[5]
    ie_type = ""
    if transaction_amount.__contains__("-"):
        ie_type = BotButton.cost
    else:
        ie_type = BotButton.receive
    user_data[UserData.sapta_ie_type] = ie_type
    jiban_logger.info("{}, \n\n{}, \n\n{}, {}, {},".format(
        transaction_type,
        transaction_amount,
        remain,
        account_number,
        date
    ))
    account_number_1 = account_number.split("*")[1]
    amount_1 = transaction_amount.split("*")[1]
    jiban_logger.info("Amount : {}".format(amount_1))
    account_number_1 = persian.convert_ar_numbers(account_number_1).replace("#", "")
    amount_1 = persian.convert_ar_numbers(amount_1).replace("-", "").replace("+", "").replace(",", "")
    user_data[UserData.spata_transaction_type] = transaction_type
    user_data[UserData.spata_remain] = remain
    user_data[UserData.spata_date] = date
    reply_keyboard = [[
        BotButton.yes_set,
        BotButton.edit_transaction_type,
        BotButton.add_description,
        BotButton.main_menu]
    ]
    text = BotMessage.sapta_message_format.format(
        name=name,
        ie_type=ie_type,
        transaction_type=transaction_type,
        account_number=account_number,
        date=date,
        amount=transaction_amount
    )
    user_data[UserData.spata_transaction_amount] = int(amount_1)
    user_data[UserData.spata_account_number] = int(account_number_1)

    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 26


def set_transaction_from_sapta(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    sapta_account_number = user_data[UserData.spata_account_number]
    all_account = get_accounts_of_user(chat_id)
    account_flag = False
    for account in all_account:
        if isinstance(account, BankAccount):
            if account.account_number:
                jiban_logger.info("Account : {}".format(account.account_number))
                if int(account.account_number) == int(sapta_account_number):
                    user_data[UserData.account] = account
                    account_flag = True

    if account_flag:
        return send_sapta_done(bot, update, user_data)
    else:
        return get_name(bot, update)


def send_sapta_done(bot, update, user_data):
    starter_checker(bot, update, user_data)
    chat_id = _get_chat_id(update)
    name = get_user_name(chat_id)
    jiban_logger.info("User Data : {}".format(user_data))
    transaction_type = user_data[UserData.spata_transaction_type].replace("#", "").replace("*", "")
    transaction_amount = user_data[UserData.spata_transaction_amount]
    sapta_ie_type = user_data[UserData.sapta_ie_type]
    sapta_account_number = user_data[UserData.spata_account_number]
    kind = None
    if sapta_ie_type == BotButton.cost:
        kind = IEText.deposit
    else:
        kind = IEText.withdraw
    account = user_data[UserData.account]
    add_income_and_expenses(chat_id=chat_id,
                            account=account,
                            type=transaction_type,
                            kind=kind,
                            amount=transaction_amount)
    text = BotMessage.sapta_saved.format(
        name=name,
        ie_type=sapta_ie_type,
        transaction_type=transaction_type,
        account_number=persian.convert_en_numbers(sapta_account_number),
        amount=_formatter(int(transaction_amount)),
        remain=_formatter(account.remain),
        account_name=account.bank_name
    )
    reply_keyboard = [[BotButton.main_menu]]
    bot.send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup(
                         reply_keyboard,
                         one_time_keyboard=True))
    return 0


def starter_checker(bot, update, user_data):
    message = _get_message(update)
    if message == BotButton.main_menu:
        return start(bot, update, user_data)


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
