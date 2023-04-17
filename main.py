from typing import Annotated
from fastapi import FastAPI, Form
import uvicorn
from database.connection import create_all, new_session
from database.models.subscriber import Subscriber

app = FastAPI()

create_all()


@app.post('/register')
async def register(email: Annotated[str, Form()]):
    new_sub = Subscriber(email=email)
    session = new_session()
    session.add(new_sub)
    session.commit()
    return {"message": "You are now subscribed to swaron.io"}


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )
