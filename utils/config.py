import os


class JibanConfig:
    db_user = os.environ.get('POSTGRES_USER', None)
    db_password = os.environ.get('POSTGRES_PASSWORD', None)
    db_host = os.environ.get('POSTGRES_HOST', None)
    db_name = os.environ.get('POSTGRES_DB', None)
    db_port = os.environ.get('POSTGRES_PORT', None)
    database_url = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name) or None
    base_url = os.getenv("BASE_URL", "https://tapi.bale.ai/")
    bot_token = os.getenv('TOKEN', "1892937244:a7938e8e605121bfb26cb8b953f4a6304551d6cc")
    poll_interval = int(os.getenv("POLL_INTERVAL", 1))
