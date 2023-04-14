from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import session
from database.connection import db
import uvicorn
from configs.environment import Environment
from database.models.contact_schema import LandingEmail

app = FastAPI()
db.connect()

@app.get('/')
def read_root():
    size = len('pedro_gonsalves@hotmail.com')
    return {"FODASE":size}

@app.post('/email/{email}')
async def emailInsert(email: str):
    newLandingEmail = LandingEmail.create(email=email)
    print(email)
    return {
        "status":"SUCCESS",
    }

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )