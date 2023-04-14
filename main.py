from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from database.models.contact_schema import landingEmail
from database.connection import Database

def getDb():
    db = Database()._session
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get('/')
async def read_root():
    size = len('pedro_gonsalves@hotmail.com')
    return {"FODASE":size}

@app.post('/email/{email}')
async def emailInsert(email: Request):
    req_info = await email.json()
    email = req_info[0].get('email')
    print(email)
    return {
        "status":"SUCCESS",
    }