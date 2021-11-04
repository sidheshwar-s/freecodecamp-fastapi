from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>\:<password>@<ip-address/hostname>/<database_name>'
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user_name}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush = False,bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()