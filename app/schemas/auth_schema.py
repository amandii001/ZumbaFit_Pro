from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.username and not self.email:
            raise ValueError("Either username or email is required")

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    message: str

class AdminResponse(BaseModel):
    admin_id: int
    username: str
    role: str
    message: str
