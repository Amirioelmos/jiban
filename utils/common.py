
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

jiban_logger = logging.getLogger(__name__)


def _get_chat_id(update):
    return update.message.chat_id

