from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(Task)).all()
    return users


@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


@router.post("/create")
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    new_task = {
        "title": task.title,
        "content": task.content,
        "priority": task.priority,
        "user_id": user.id,
        "slug": slugify(task.title)  # slug generation
    }
    db.execute(insert(Task).values(new_task))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{task_id}")
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    stmt = (update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority
    ))

    result = db.execute(stmt)

    # check if any rows been touched
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    db_task = db.scalar(select(Task).where(Task.id == task_id))

    if db_task is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
