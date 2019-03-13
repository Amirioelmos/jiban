
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
    cash_amount = "cash_amount"
    cash_name = "cash_name"
    account_type = "account_type"
