from app.db.models import tasks
from app.db.base import database

async def clean_completed():
    await database.execute(tasks.delete().where(tasks.c.completed == True))
