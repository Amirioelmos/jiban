from handlers_manager import handlers_manager
from bot import updater, dp
from utils.config import JibanConfig


if __name__ == '__main__':
    handlers_manager(dp=dp)
    updater.start_polling(JibanConfig.poll_interval)
    updater.idle()