from sqlmodel import SQLModel,Field
from typing import Optional
import shortuuid
from datetime import datetime

class NewsPost(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: str
    attachment_url: Optional[str] = None