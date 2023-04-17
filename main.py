from fastapi import FastAPI, HTTPException
from database.connection import db
import uvicorn
from configs.environment import Environment
import re

app = FastAPI()

Environment.load_environment()
db.connect()
db.create_table()

@app.post('/email/{email}')
async def emailInsert(email:str):
    pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    validateEmail = re.match(pattern,email)
    if validateEmail != None:

        query = db.exec_dql_comm(f"""
                    select 1 as check from contact.landing_email where email = '{email}'
        """)

        if len(query.fetchall()) == 0:
            db.exec_dml_com(f"""
            insert into contact.landing_email (email) values ('{email}')
            """)
            return HTTPException(status_code=200,detail="Email entered successfully.")

        else:
            raise HTTPException(status_code=409, detail="Email already registered.")

    else:
        raise HTTPException(status_code=400, detail="Please enter a valid email.")


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )