from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def get_main_page() -> str:
    return "Main page"


@app.get("/user/admin")
async def get_admin_page() -> str:
    return "You logged in as administrator"


@app.get("/user/{user_id}")
async def get_main_page(user_id: int = Path(
    ge=1,
    le=100,
    description="Enter User ID",
    example="1"
)) -> str:
    return f"You logged in as user № {user_id}"


@app.get("/user/{username}/{age}")
# The Annotation doesn't really need it here since we cover both parameters 'username' and 'age' with Path
async def get_user_info(username: Annotated[str, Path(
    min_length=5,
    max_length=20,
    description="Enter username",
    example="UrbanUser"

)], age: Annotated[int, Path(
    ge=18,
    le=120,
    description="Enter age",
    example=24
)]) -> str:
    return f"User info. Name: {username}, Age: {age}"
