from sqlalchemy import event
from functools import wraps
from app.logger import logger

# Uma lista simples para servir como o nosso registo de listeners.
_listeners = []


def listens_for(model, identifier):
    """
    Um decorador que regista uma função como um listener para um evento
    do SQLAlchemy, adicionando-a a um registo para ser processada mais tarde.
    """

    def decorator(func):
        # Adiciona a informação do listener à nossa lista de registo.
        _listeners.append((model, identifier, func))

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def register_sqlalchemy_listeners():
    """
    Itera sobre o nosso registo e ativa cada listener usando event.listen().
    """
    logger.info("A registar os listeners do SQLAlchemy...")
    for model, identifier, func in _listeners:
        event.listen(model, identifier, func)
        logger.info(
            f"-> Listener '{func.__name__}' registado para o evento '{identifier}' no modelo '{model.__name__}'"
        )
    logger.info("Registo de listeners concluído.")


def remove_sqlalchemy_listeners():
    """
    Remove todos os listeners registados. Útil durante o encerramento da aplicação.
    """
    logger.info("A remover os listeners do SQLAlchemy...")
    for model, identifier, func in _listeners:
        event.remove(model, identifier, func)
    logger.info("Remoção de listeners concluída.")
