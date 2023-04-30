from unittest.mock import MagicMock, Mock

import pytest
from email_validator import EmailNotValidError

from database.models.subscriber import Subscriber
from email_service.landing_page import UserAlreadySubscribed, register


def test_register_when_email_already_subscribed(db_session):
    db_session.add(Subscriber(email="foo@swaron.io"))
    with pytest.raises(UserAlreadySubscribed):
        register("foo@swaron.io", db_session, None)


def test_register_when_email_is_not_subscribed(db_session):
    email_sender = MagicMock(return_value=True)
    register("foo@swaron.io", db_session, email_sender)
    subscribed_user = (
        db_session.query(Subscriber).filter(Subscriber.email == "foo@swaron.io").first()
    )
    assert subscribed_user.email == "foo@swaron.io"


def test_register_email_when_sending_email_fails(db_session):
    email_sender = Mock(side_effect=EmailNotValidError)
    with pytest.raises(EmailNotValidError):
        register("foo@swaron.io", db_session, email_sender)

    already_subscribed = db_session.query(
        db_session.query(Subscriber)
        .filter(Subscriber.email == "foo@swaron.io")
        .exists()
    ).scalar()
    assert not already_subscribed
