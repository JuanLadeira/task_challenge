from sqlmodel import select
from typing import List, Annotated

from fastapi import Depends
from app.db import DBSession
from app.todo.models import Todo


class TodoService:
    """
    Esta classe encapsula a lógica de negócio para manipulação de tarefas.
    Todas as interações com o banco de dados relacionadas a tarefas devem passar por aqui.
    """

    def __init__(self, session: DBSession):
        """
        Inicializa o serviço com uma sessão de banco de dados.

        Args:
            session: Uma sessão do SQLModel para interagir com o banco de dados.
        """
        self.session = session

    def get_all_todos(self) -> List[Todo]:
        """Busca todas as tarefas, ordenadas por ID."""
        todos = self.session.exec(select(Todo).order_by(Todo.id)).all()
        return todos

    def create_todo(self, content: str) -> Todo:
        """Cria uma nova tarefa."""
        todo = Todo(content=content)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def update_todo_status(self, todo_id: int) -> Todo | None:
        """
        Encontra uma tarefa pelo ID e alterna seu estado 'completed'.
        Retorna a tarefa atualizada ou None se não for encontrada.
        """
        todo = self.session.get(Todo, todo_id)
        if todo:
            todo.completed = not todo.completed
            self.session.add(todo)
            self.session.commit()
            self.session.refresh(todo)
        return todo

    def delete_todo_by_id(self, todo_id: int) -> bool:
        """
        Deleta uma tarefa pelo seu ID.
        Retorna True se a tarefa foi deletada, False caso contrário.
        """
        todo = self.session.get(Todo, todo_id)
        if todo:
            self.session.delete(todo)
            self.session.commit()
            return True
        return False


def get_todo_service(
    # A dependência da sessão agora é explícita usando Annotated
    session: DBSession,
) -> TodoService:
    """
    Cria e retorna uma instância do TodoService com a sessão
    de banco de dados injetada.
    """
    return TodoService(session)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]


def create_todo_example(service: TodoServiceDep) -> Todo:
    """
    Função de exemplo para criar uma tarefa.
    Esta função pode ser usada para testes ou como um exemplo de uso do serviço.
    """
    return service.create_todo(content="Exemplo de tarefa")
