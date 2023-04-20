from fastapi import FastAPI,HTTPException, Body
import uvicorn
from sqlalchemy.exc import IntegrityError
from database.connection import create_all, new_session
from database.models.subscriber import Subscriber
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError

app = FastAPI()

create_all()

@app.post('/register')
async def register(body = Body(...)):
    email = body.get("email")
    try:
        validate_email(email, check_deliverability=False)
        
        db = new_session()
        subscriber = Subscriber(email=email)
        db.add(subscriber)
        db.commit()
        
        return {"message": "Email registered successfully."}
    except IntegrityError:
        return HTTPException(status_code=409, detail="Email already registered.")
    except EmailSyntaxError or EmailNotValidError:
        return HTTPException(status_code=406, detail="Email format is not valid.",headers=None)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )