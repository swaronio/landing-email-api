import os
from fastapi import FastAPI, HTTPException, Body
import uvicorn
from sqlalchemy.exc import IntegrityError
from database.connection import create_all, new_session
from database.models.subscriber import Subscriber
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
import smtplib
from email.message import EmailMessage

app = FastAPI()

create_all()

@app.post('/register', status_code=201)
async def register(body = Body(...)):
    email = body.get("email")
    try:
        validate_email(email, check_deliverability=False)
        
        db = new_session()

        subscriber_exists = db.query(Subscriber).filter(Subscriber.email == email).first()

        if subscriber_exists:
            raise HTTPException(status_code=409, detail="Email already registered.")

        subscriber = Subscriber(email=email)
        db.add(subscriber)

        # Send email
        mailserver = smtplib.SMTP('smtp.zoho.com', 587)
        mailserver.starttls()
        mailserver.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))

        msg = EmailMessage()
        msg.set_content("Hello, welcome to swaron.io! \n\nWe are a educational platform that aims to help students to learn computer science for free. \n\nWe are still in development, but we will send you an email when we launch. \n\nThank you for your support! \n\nSwaron Team")
        msg['Subject'] = "Hello, welcome to swaron.io!"
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = email

        mailserver.send_message(msg)

        db.commit()

        mailserver.quit()
        
        return {"message": "Email registered successfully."}
    except EmailSyntaxError or EmailNotValidError:
        raise HTTPException(status_code=406, detail="Email format is not valid.",headers=None)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )