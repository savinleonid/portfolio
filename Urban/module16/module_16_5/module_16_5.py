from pydantic import BaseModel
from typing import Annotated

from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str = None
    age: int = None


@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(
    min_length=5,
    max_length=20,
    description="Enter username",
    example="UrbanUser"

)], age: Annotated[int, Path(
    ge=18,
    le=120,
    description="Enter age",
    example=24
)]) -> User:
    user = User()
    user_id = len(users) + 1
    user.id = user_id
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int = Path(
    ge=1,
    le=100,
    description="Enter User ID",
    example="1"
), username: str = Path(
    min_length=5,
    max_length=20,
    description="Enter username",
    example="UrbanUser"
), age: int = Path(
    ge=18,
    le=120,
    description="Enter age",
    example=24
)) -> User:
    try:
        user: User = users[user_id-1]
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(
    ge=1,
    le=100,
    description="Enter User ID",
    example="1"
)) -> User:
    try:
        for user in users:
            if user.id == user_id:
                return users.pop(user_id-1)
        else:
            raise IndexError()
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
