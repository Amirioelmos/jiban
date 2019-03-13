from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import JibanConfig

engine = create_engine(JibanConfig.database_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()