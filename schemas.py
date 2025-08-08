from pydantic import BaseModel
from typing import Optional
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    group: Optional[str] = None
    gender: str