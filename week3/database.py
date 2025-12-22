from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

MYSQL_CONNECTION_STRING = "mysql+pymysql://app_user:app_pass@localhost:3306/app_db"

engine = create_engine(MYSQL_CONNECTION_STRING)
Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)