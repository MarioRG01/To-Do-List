from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.db.base import database
from app.db.models import tasks
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="", tags=["tasks"])

@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskCreate,
        user=Depends(get_current_user)
    ):
        insert_query = tasks.insert().values(
            user_id=user["id"],
            title=task.title,
            description=task.description
        )
        insert_query = tasks.insert().values(
            user_id=user["id"],
            title=task.title,
            description=task.description,
            completed=False               # <-- aquí
        )
        task_id = await database.execute(insert_query)
        select_query = tasks.select().where(tasks.c.id == task_id)
        row = await database.fetch_one(select_query)
        return row


@router.get("/tasks", response_model=List[TaskRead])
async def list_tasks(user=Depends(get_current_user)):
    select_query = tasks.select().where(tasks.c.user_id == user["id"])
    rows = await database.fetch_all(select_query)
    return rows

@router.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user=Depends(get_current_user)
):
    select_query = tasks.select().where(tasks.c.id == task_id)
    row = await database.fetch_one(select_query)
    if not row or row["user_id"] != user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    update_query = (
        tasks.update()
             .where(tasks.c.id == task_id)
             .values(completed=task_update.completed)
    )
    await database.execute(update_query)
    updated = await database.fetch_one(select_query)
    return updated
