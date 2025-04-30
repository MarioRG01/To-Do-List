from fastapi import FastAPI
from app.db.base import database
from app.routers import auth, tasks  

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Routers
app.include_router(auth.router)
