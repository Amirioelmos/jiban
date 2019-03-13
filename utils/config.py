import os


class JibanConfig:
    base_url = os.getenv("BASE_URL", "https://tapi.bale.ai/")
    bot_token = os.getenv('TOKEN', "1892937244:a7938e8e605121bfb26cb8b953f4a6304551d6cc")
    poll_interval = int(os.getenv("POLL_INTERVAL", 2))
