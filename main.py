from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import session
from sqlalchemy import insert
from database.connection import db
import uvicorn
from configs.environment import Environment
from database.models.contact_schema import LandingEmail

app = FastAPI()

Environment.load_environment()
db.connect()

@app.get('/')
def read_root():
    size = len('pedro_gonsalves@hotmail.com')
    return {"FODASE":size}

@app.post('/email/{email}')
async def emailInsert(email: str):
    insert_res = db.exec_dml_com(
        insert(LandingEmail).values(
            email=email
        )
    )
    db._session.add(insert_res)
    db._session.commit()

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