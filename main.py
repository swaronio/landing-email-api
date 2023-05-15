import os
from dotenv import load_dotenv
import uvicorn
from email_validator import EmailNotValidError, validate_email
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database.connection import create_all, new_engine, new_session
from database.models.subscriber import Subscriber
from email_service.landing_page import UserAlreadySubscribed, register_user, send_email

load_dotenv()

engine = new_engine()
create_all(engine)
Session = new_session(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", status_code=201)
async def register(body=Body(...)):
    try:
        email = body["email"]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Email field expected.") from exc

    try:
        validate_email(email, check_deliverability=False)

        db = Session()

        try:
            register_user(email, db, send_email)
        except UserAlreadySubscribed as exc:
            raise HTTPException(
                status_code=409, detail="Email already registered."
            ) from exc

        return {"message": "Email registered successfully."}
    except EmailNotValidError as exc:
        raise HTTPException(
            status_code=406, detail="Email format is not valid."
        ) from exc


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("SERVER_DEBUG") == "True",
        log_level="info",
    )
