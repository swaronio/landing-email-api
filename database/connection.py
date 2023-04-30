from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def new_engine():
    return create_engine("sqlite+pysqlite:///swaron.db", echo=True)


engine = new_engine()


def new_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def create_all():
    Base.metadata.create_all(engine)
