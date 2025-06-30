from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import func

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        index=True, unique=True, max_length=50, min_length=3)
    password: str
    email: str = Field(
        index=True, unique=True, max_length=100, min_length=5)
    created_at: datetime = Field(
        default_factory=func.now, 
        nullable=False
        )
    todos: list["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
