from sqlmodel import SQLModel



class TodoCreate(SQLModel):
    """Schema para a criação de uma nova tarefa. Apenas o conteúdo é necessário."""
    content: str


class TodoUpdate(SQLModel):
    """Schema para a atualização de uma tarefa. Ambos os campos são opcionais."""
    content: str | None = None
    completed: bool | None = None
