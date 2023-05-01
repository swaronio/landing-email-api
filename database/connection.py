import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def new_engine():
    url = URL.create(
        "mysql+mysqlconnector",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
    )
    return create_engine(url, echo=True)


def new_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all(engine):
    Base.metadata.create_all(engine)
