import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from test.factories.todo import TodoFactory
from pytest_factoryboy import register

# --- Definição de Variáveis de Ambiente para Teste ---
# ATENÇÃO: Isto deve ser feito ANTES de importar a sua aplicação (app.main, app.db, etc.)
# para garantir que o Pydantic as lê no arranque.
os.environ['SECRET_KEY'] = 'test_secret_key_for_testing_purposes'
os.environ['ALGORITHM'] = 'HS256'
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '30'

# Agora que as variáveis estão definidas, podemos importar o resto.
from app.main import app
from app.db import get_session



# --- Configuração da Base de Dados de Teste ---

# Usamos uma base de dados SQLite em memória para os testes.
# 'StaticPool' e 'connect_args' são necessários para garantir que a mesma
# conexão seja usada em todos os acessos, o que é um requisito para o SQLite em memória.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

# --- Fixture para a Sessão da Base de Dados de Teste ---
@pytest.fixture(name="session")
def session_fixture():
    """
    Esta fixture cria as tabelas na base de dados de teste antes de cada teste,
    fornece uma sessão e depois limpa as tabelas após o teste.
    """
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

# --- Fixture para o Cliente de Teste ---

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Esta fixture cria um TestClient para a sua aplicação, mas antes
    sobrescreve a dependência `get_session` para usar a nossa sessão de teste.
    """
    def get_test_session():
        # A nossa dependência de teste simplesmente retorna a sessão
        # criada pela fixture 'session_fixture'.
        yield session

    # Sobrescreve a dependência na aplicação
    app.dependency_overrides[get_session] = get_test_session
    
    # Cria o cliente de teste
    with TestClient(app) as client:
        yield client
    
    # Limpa as sobrescrições de dependência após o teste
    app.dependency_overrides.clear()


@pytest.fixture
def todo_factory(session: Session) -> type[TodoFactory]:
    """
    Fixture que fornece a TodoFactory já configurada com a sessão de teste.
    """
    # Associa a fábrica à sessão de teste atual
    TodoFactory._meta.sqlalchemy_session = session
    return TodoFactory
