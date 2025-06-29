import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.user.models import User
from app.db import DBSession  # Importe sua sessão de banco de dados aqui


class UserFactory(SQLAlchemyModelFactory):
    """
    Fábrica para criar instâncias do modelo User para testes.
    Utiliza factory-boy com Faker para gerar dados realistas.
    """

    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"
    
    username = factory.Faker("user_name")
    
    email = factory.Faker("safe_email")
    
    password = "test_password123"


def create_user_for_testing(session: DBSession, username=None) -> User:
    """
    Função de exemplo que demonstra como usar a fábrica.
    
    Args:
        session: A sessão de banco de dados de teste.
    
    Returns:
        Uma nova instância de User, já persistida no banco de dados.
    """
    # Associa a sessão de teste à fábrica antes de usá-la.
    UserFactory._meta.sqlalchemy_session = session
    
    # Cria (e salva) um novo usuário com dados falsos.
    if username:
        user = UserFactory.create(session=session, username=username)
    else:
        user = UserFactory.create(session=session)
    
    return user

def create_multiple_users(session: DBSession, count: int = 5) -> list[User]:
    """Cria múltiplos usuários para testes de listagem."""
    UserFactory._meta.sqlalchemy_session = session
    
    # Usa a função 'create_batch' da factory para criar vários usuários de uma vez.
    users = UserFactory.create_batch(session=session, size=count)
    
    return users
