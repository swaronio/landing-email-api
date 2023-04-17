from typing import Any
from sqlalchemy import MetaData,create_engine, schema
from sqlalchemy.engine import CursorResult
from configs.environment import Environment

class Database:
    def __init__(self):
        self._engine = None
        self._base = None
        self._meta = None
        self._session = None

    def connect(self):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker

        self._engine = create_engine(url=f"postgresql://{Environment.DB_USER}:{Environment.DB_PASSWORD}@{Environment.DB_HOST}:{str(Environment.DB_PORT)}/{Environment.DB_NAME}",
                               echo=True)
        Base = declarative_base()
        SessionLocal = sessionmaker(bind=self._engine)
        session = SessionLocal()

        #schemas in the list are validated and if they do not exist in the database they are created
        schemas = ['contact']
        for schemaName in schemas:
            if not self._engine.dialect.has_schema(self._engine, schemaName):
                self._engine.execute(schema.CreateSchema(schemaName))

        self._base = Base
        self._meta = MetaData()
        self._session = session

    def exec_dml_com(self,query:Any):
        with self._engine.connect() as conn:
            conn.execute(query)

    def exec_dql_comm(self,query:Any) -> CursorResult:
        with self._engine.connect() as conn:
            result = conn.execute(query)
        return result


    def create_table(self):
        #metadata variable is responsible for migrating the landingEmail object to the db
        from models.contact_schema import metadata
        metadata

db = Database()