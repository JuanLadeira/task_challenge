from sqlmodel import SQLModel, Field, Relationship
from typing import Optional



class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    completed: bool = False

    # 1. Adiciona a coluna para armazenar o ID do usuário
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # 2. Adiciona a referência de volta para o objeto User
    user: Optional["User"] = Relationship(back_populates="todos")