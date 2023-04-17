from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def new_engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True)

engine = new_engine()

def new_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

def create_all():
    Base.metadata.create_all(engine)
