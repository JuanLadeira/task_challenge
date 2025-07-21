from sqlmodel import SQLModel
import datetime
from typing import Optional


class UserCreate(SQLModel):
    """Schema para criar um novo usuário. Requer todos os campos."""

    username: str
    email: str
    password: str


class UserUpdate(SQLModel):
    """
    Schema para atualizar um usuário. Todos os campos são opcionais.
    Apenas os campos fornecidos na requisição serão atualizados.
    """

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None  # Opcional para permitir a troca de senha.


class UserPublic(SQLModel):
    """
    Schema para retornar os dados de um usuário de forma segura.
    NÃO inclui a senha.
    """

    id: int
    username: str
    email: str
    created_at: datetime.datetime
