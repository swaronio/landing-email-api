from database.connection import Database
from sqlalchemy import func
from sqlalchemy import Column,Integer,String,DateTime, MetaData, Table, ForeignKey

engine = Database()._engine
metadata = MetaData()

LandingEmail = Table(
    'landing_email',
    metadata,
    Column("email", String(60)),
    Column("created_at", DateTime,server_default=func.now()),
    schema='contact'
)