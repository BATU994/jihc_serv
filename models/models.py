from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from typing import Optional

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    name: Optional[str] = None
    group: Optional[str] = None