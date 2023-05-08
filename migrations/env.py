from logging.config import fileConfig
import os
from sqlalchemy import MetaData, create_engine
from alembic import context
from database.connection import new_engine

engine = new_engine()
metadata = MetaData()
metadata.bind = engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#url connection
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')



db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"


def run_migrations_online() -> None:

    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()