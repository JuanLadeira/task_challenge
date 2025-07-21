import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.todo.models import Todo


class TodoFactory(SQLAlchemyModelFactory):
    """
    Fábrica para o modelo Todo, para gerar dados de teste.
    A integração com a sessão de teste do SQLModel é feita no conftest.py.
    """

    class Meta:
        model = Todo
        # A sessão será injetada dinamicamente pela fixture do pytest
        sqlalchemy_session = None
        # 'flush' é recomendado para garantir que os IDs estão disponíveis sem um commit completo
        sqlalchemy_session_persistence = "flush"

    # Define como gerar valores para cada campo do modelo
    id = factory.Sequence(lambda n: n + 1)
    content = factory.Faker("sentence", nb_words=4, locale="pt_PT")
    completed = factory.Faker("boolean")
