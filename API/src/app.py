from fastapi import FastAPI
from src.routes.person import router as PersonRouter

app = FastAPI()
app.include_router(PersonRouter, tags=['Person'], prefix='/person')

@app.get('/test')
async def root():
    return {'Hello': "World"}