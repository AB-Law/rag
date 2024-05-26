
from pydantic import BaseModel, Field

class UserOut(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str = Field(..., description="The username for the new user. It must be unique.")
    full_name: str = Field(..., description="The full name of the new user.")
    email: str = Field(..., description="The email address of the new user.")
    password: str = Field(..., description="The password for the new user. It must be at least 8 characters long.")
