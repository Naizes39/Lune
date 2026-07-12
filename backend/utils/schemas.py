# utils/schemas.py
# File contating schemas for agents


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated, Literal
import uuid


class Message(BaseModel):
    message_id: Annotated[str, Field(default_factory = lambda: str(uuid.uuid4()))]
    role: Literal["user", "assistant", "system"] = "user"
    content: Annotated[str, Field(min_length = 1, max_length = 50000)]
    time_sent: Annotated[datetime, Field(default_factory = lambda: datetime.now())]
    session_id: str
    user_id: str


class Skill(BaseModel):
    skill_id: Annotated[str, Field(default_factory = lambda: str(uuid.uuid4()))]
    name: Annotated[str, Field(min_length = 1, max_length = 50)]
    category: Annotated[str, Field(min_length = 1, max_length = 100)]
    description: Annotated[str, Field(min_length = 1, max_length = 200)]
    permissions_needed: Annotated[bool, Field(default = False)]


class Session(BaseModel):
    session_id: Annotated[str, Field(default_factory = lambda: str(uuid.uuid4()))]
    user_id: str
    creation_date: Annotated[datetime, Field(default_factory = lambda: datetime.now())]
    status: Literal["active", "paused", "crashed", "ended"] = "active"
