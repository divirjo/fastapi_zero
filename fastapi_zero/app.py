from fastapi import FastAPI

from fastapi_zero.schemas import Message


app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
