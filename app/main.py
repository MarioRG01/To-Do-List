# app/main.py
from fastapi import FastAPI
from app.db.base import database, engine, metadata
from app.routers import auth, tasks   

app = FastAPI()

@app.on_event("startup")
async def startup():
    metadata.create_all(bind=engine)  
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth.router)
app.include_router(tasks.router)
