from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.get("/{user_id}/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id))
    if tasks is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return tasks


@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = {
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "age": user.age,
        "slug": slugify(user.username)  # slug generation
    }
    db.execute(insert(User).values(new_user))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = (update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age
    ))

    result = db.execute(stmt)

    # check if any rows been touched
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")

    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
