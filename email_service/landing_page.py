import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

import requests
from PIL import Image

from database.models.subscriber import Subscriber


class UserAlreadySubscribed(Exception):
    pass


def register_user(email: str, db, email_sender):
    already_subscribed = db.query(
        db.query(Subscriber).filter(Subscriber.email == email).exists()
    ).scalar()
    if already_subscribed:
        raise UserAlreadySubscribed

    subscriber = Subscriber(email=email)

    try:
        db.add(subscriber)
        email_sender(email)
    except:
        db.rollback()
        raise
    else:
        db.commit()


def send_email(to: str):
    response = requests.get("https://i.ibb.co/h28SwBQ/swaron-2.jpg")
    img = Image.open(BytesIO(response.content))

    mailserver = smtplib.SMTP(os.getenv("EMAIL_SERVER"), 587)
    mailserver.starttls()
    mailserver.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    message = MIMEMultipart("related")
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = to
    message["Subject"] = "Welcome to Swaron!"

    msg_alternative = MIMEMultipart("alternative")
    message.attach(msg_alternative)

    msg_text = MIMEText(
        '<center><br><img src="cid:image1" width="350" height="auto"><br></center>',
        "html",
    )

    msg_alternative.attach(msg_text)

    img_io = BytesIO()
    img.save(img_io, "JPEG")
    img_io.seek(0)
    image = MIMEImage(img_io.read())
    image.add_header("Content-ID", "<image1>")
    message.attach(image)

    mailserver.sendmail(os.getenv("EMAIL_USER"), to, message.as_string())
    mailserver.quit()
