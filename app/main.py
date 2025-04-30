from fastapi import FastAPI
from app.db.base import database, engine, metadata
from app.routers import auth, tasks

# 1) Importa APScheduler y tu limpiador
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.background.cleaner import clean_completed

app = FastAPI()

@app.on_event("startup")
async def startup():
    metadata.create_all(bind=engine)
    await database.connect()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clean_completed, 'interval', minutes=10)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth.router)
app.include_router(tasks.router)
