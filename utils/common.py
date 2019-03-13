
import logging

import persian

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

jiban_logger = logging.getLogger(__name__)


def _get_chat_id(update):
    return update.message.chat_id


def _get_message(update):
    return update.message.text

def _formatter(_id):
    try:
        return persian.convert_en_numbers("{:,}".format(_id))
    except Exception as e:
        return _id

class UserData:
    cost_account = "cost_account"
    cost_date = "cost_date"
    cost_amount = "cost_amount"
    cost_type = "cost_type"
    back_account_account_number = "back_account_account_number"
    back_account_cart_number = "back_account_cart_number"
    bank_account_remain = "bank_account_remain"
    bank_name = "bank_name"
    cash_amount = "cash_amount"
    cash_name = "cash_name"
    account_type = "account_type"
