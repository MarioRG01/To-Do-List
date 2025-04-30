from fastapi import FastAPI
from app.db.base import database, engine, metadata
from app.routers import auth, tasks  # tasks vendrá luego

app = FastAPI()

@app.on_event("startup")
async def startup():
    # 1) Crea las tablas si no existen
    metadata.create_all(bind=engine)
    # 2) Conecta la BD en modo asíncrono
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth.router)
