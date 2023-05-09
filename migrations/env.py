from logging.config import fileConfig
from sqlalchemy import MetaData
from alembic import context
from database.connection import new_engine

engine = new_engine()
metadata = MetaData()
metadata.bind = engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_online() -> None:
    connectable = new_engine()

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
