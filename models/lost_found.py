from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime,timezone
from uuid import uuid4

class LostFoundPost(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    type: str
    item_name: str
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    image_path: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author_id: str  