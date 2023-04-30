import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base
from database.models.subscriber import Subscriber
from email_service.landing_page import UserAlreadySubscribed, register


class TestRegister:
    @classmethod
    def setup_class(cls):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)
        cls.db = sessionmaker(bind=engine)()

    @classmethod
    def teardown_class(cls):
        cls.db.rollback()
        cls.db.close()

    def test_register_when_email_already_subscribed(self):
        self.db.add(Subscriber(email="foo@swaron.io"))
        with pytest.raises(UserAlreadySubscribed):
            register("foo@swaron.io", self.db)
