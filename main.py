from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import session
from database.connection import Database
import uvicorn
from configs.environment import load_environment, Environment

def getDb():
    db = Database()._session
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

load_environment()
print(Environment.DB_USER)

@app.get('/')
def read_root():
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

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )