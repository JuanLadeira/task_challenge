from app.todo.models import Todo
from app.logger import logger
from app.events import listens_for


@listens_for(Todo, "after_insert")
def after_todo_insert(mapper, connection, target: Todo):
    """
    Este 'listener' é executado depois de um objeto Todo ser inserido.
    """
    logger.info(
        f"Nova tarefa criada com ID: {target.id} e Conteúdo: '{target.content}'"
    )


@listens_for(Todo, "after_update")
def after_todo_update(mapper, connection, target: Todo):
    """Este 'listener' é executado depois de um objeto Todo ser atualizado."""
    logger.info(
        f"Tarefa com ID {target.id} foi atualizada. Novo estado 'completed': {target.completed}"
    )


@listens_for(Todo, "after_delete")
def after_todo_delete(mapper, connection, target: Todo):
    """Este 'listener' é executado depois de um objeto Todo ser deletado."""
    logger.info(f"Tarefa com ID {target.id} foi deletada.")
