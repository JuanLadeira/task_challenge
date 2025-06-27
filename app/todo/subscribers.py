from app.todo.models import Todo
from app.logger import logger
from app.events import listens_for


@listens_for(Todo, 'after_insert')
def after_todo_insert(mapper, connection, target: Todo):
    """
    Este 'listener' é executado depois de um objeto Todo ser inserido.
    """
    logger.info(f"--- Evento 'after_insert' despoletado para Todo ---")
    logger.info(f"Nova tarefa criada com ID: {target.id} e Conteúdo: '{target.content}'")
    logger.info(f"Ação simulada: Enviar notificação ou email...")
    logger.info(f"-------------------------------------------------")

@listens_for(Todo, 'after_update')
def after_todo_update(mapper, connection, target: Todo):
    """Este 'listener' é executado depois de um objeto Todo ser atualizado."""
    logger.info(f"--- Evento 'after_update' despoletado para Todo ---")
    logger.info(f"Tarefa com ID {target.id} foi atualizada. Novo estado 'completed': {target.completed}")
    logger.info(f"-------------------------------------------------")

@listens_for(Todo, 'after_delete')
def after_todo_delete(mapper, connection, target: Todo):
    """Este 'listener' é executado depois de um objeto Todo ser deletado."""
    logger.info(f"--- Evento 'after_delete' despoletado para Todo ---")
    logger.info(f"Tarefa com ID {target.id} foi deletada.")
    logger.info(f"-------------------------------------------------")