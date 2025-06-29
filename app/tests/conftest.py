import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.db import get_session
from app.tests.factories.todo import TodoFactory
from testcontainers.postgres import PostgresContainer

@pytest.fixture
def session():
    with PostgresContainer("postgres:16", driver="psycopg2") as postgres:
        engine = create_engine(postgres.get_connection_url())
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
        SQLModel.metadata.drop_all(engine)


# --- Client Fixture for API Testing ---
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def todo_factory(session: Session) -> type[TodoFactory]:
    """
    Fixture que fornece a TodoFactory já configurada com a sessão de teste.
    """
    # Associa a fábrica à sessão de teste atual
    TodoFactory._meta.sqlalchemy_session = session
    return TodoFactory
