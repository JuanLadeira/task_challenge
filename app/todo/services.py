from sqlmodel import select
from typing import List, Annotated

from fastapi import Depends
from app.db import DBSession
from app.todo.models import Todo
from app.todo.schemas import TodoUpdate


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

    def get_all_todos(self, user_id=None) -> List[Todo]:
        """Busca todas as tarefas, ordenadas por ID."""
        if user_id:
            return self.session.exec(select(Todo).where(Todo.user_id==user_id).order_by(Todo.id)).all()
        return self.session.exec(select(Todo).order_by(Todo.id)).all() 

    def create_todo(self, content: str, user_id=None) -> Todo:
        """Cria uma nova tarefa."""
        if user_id:
            todo = Todo(content=content, user_id=user_id)
        else:
            todo = Todo(content=content)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Todo | None:
        """
        Encontra uma tarefa pelo ID e alterna seu estado 'completed'.
        Retorna a tarefa atualizada ou None se não for encontrada.
        """
        # 1. Busca a tarefa no banco de dados
        db_todo = self.session.get(Todo, todo_id)
        if not db_todo:
            return None

        # 2. Pega os dados do Pydantic model e exclui os que não foram enviados (unset)
        update_data = todo_data.model_dump(exclude_unset=True)

        # 3. Itera sobre os dados e atualiza o objeto do banco de dados
        for key, value in update_data.items():
            setattr(db_todo, key, value)

        # 4. Salva as alterações no banco de dados
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        return db_todo

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
