
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.todo.models import Todo


def test_criar_tarefa_api(client: TestClient):
    """
    Testa a criação de uma nova tarefa através do endpoint POST /api/todos/.
    """
    # Dados da nova tarefa
    dados_tarefa = {"content": "Lavar a loiça"}
    
    # Faz a requisição POST
    response = client.post("/api/todos/", json=dados_tarefa)
    
    # Verifica o resultado
    data = response.json()
    assert response.status_code == 201  # 201 Created
    assert data["content"] == dados_tarefa["content"]
    assert data["completed"] is False
    assert "id" in data

def test_ler_todas_as_tarefas_vazio(client: TestClient):
    """
    Testa a leitura de tarefas quando a base de dados está vazia.
    """
    response = client.get("/api/todos/")
    
    assert response.status_code == 200
    assert response.json() == []

def test_ler_todas_as_tarefas_com_dados(client: TestClient, todo_factory):
    """
    Testa a leitura de tarefas depois de adicionar uma à base de dados.
    """
    # Prepara os dados de teste diretamente na base de dados
    factory = todo_factory(content="Passear o cão", completed=False)
    todo_factory.create_batch(9)
    # Faz a requisição GET
    response = client.get("/api/todos/")
    
    # Verifica o resultado
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10
    assert data[0]["content"] == factory.content

def test_ler_uma_tarefa_por_id(client: TestClient, todo_factory):
    """
    Testa a leitura de uma única tarefa pelo seu ID.
    """
    tarefa_teste = todo_factory(content="Fazer compras", completed=True)
    response = client.get(f"/api/todos/{tarefa_teste.id}")
    
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == tarefa_teste.content
    assert data["id"] == tarefa_teste.id

def test_ler_uma_tarefa_nao_encontrada(client: TestClient):
    """
    Testa a leitura de uma tarefa com um ID que não existe.
    """
    response = client.get("/api/todos/999")
    
    assert response.status_code == 404

def test_atualizar_tarefa(client: TestClient, todo_factory):
    """
    Testa a atualização de uma tarefa existente através do endpoint PUT.
    """
    tarefa_teste = todo_factory(content="Ler um livro", completed=False)
    dados_atualizacao = {"content": "Ler um livro de ficção", "completed": True}
    response = client.put(f"/api/todos/{tarefa_teste.id}", json=dados_atualizacao)
    
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == dados_atualizacao["content"]
    assert data["completed"] is True

def test_eliminar_tarefa(client: TestClient, todo_factory, session: Session):
    """
    Testa a eliminação de uma tarefa.
    """
    tarefa_teste = todo_factory(content="Limpar a casa", completed=False)

    # Faz a requisição DELETE
    response = client.delete(f"/api/todos/{tarefa_teste.id}")
    
    # Verifica que a requisição teve sucesso
    assert response.status_code == 204  # 204 No Content
    
    # Verifica que a tarefa já não existe na base de dados
    tarefa_na_db = session.get(Todo, tarefa_teste.id)
    assert tarefa_na_db is None
