import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


# Assume que você tem fixtures de teste configuradas para o client e a sessão.
# Ex: em conftest.py

@pytest.mark.users
def test_create_user_successfully(
    client: TestClient, 
    token, 
    user_factory
    ):
    """
    Testa a criação bem-sucedida de um novo usuário.
    """
    # Dados para o novo usuário
    user_build = user_factory.build()

    user_data ={
        "username": user_build.username,
        "email": user_build.email,
        "password": user_build.password
    }
    
    # Faz a requisição POST para o endpoint de criação
    response = client.post(
        "/users/", 
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
        )
    
    # Verifica o status code e o corpo da resposta
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    assert "id" in created_user
    assert "password" not in created_user # Garante que a senha não foi retornada

@pytest.mark.users
def test_create_user_with_existing_username(
    client: TestClient,
    user_factory,
    token,
    ):
    """
    Testa a falha ao tentar criar um usuário com um nome de usuário que já existe.
    """
    # 1. Cria um usuário inicial no banco de dados usando a fábrica
    user_factory(username="existinguser")
    
    # 2. Tenta criar um novo usuário com o mesmo nome
    duplicate_user_data = {
        "username": "existinguser",
        "email": "new@example.com",
        "password": "password123",
    }
    response = client.post(
        "/users/", 
        json=duplicate_user_data,
        headers={'Authorization': f'Bearer {token}'},
        )
    
    # 3. Verifica se a API retornou o erro esperado (400 Bad Request)
    assert response.status_code == 400
    assert "nome de usuário já está em uso" in response.json()["detail"]

@pytest.mark.users
def test_get_all_users(
    client: TestClient, 
    user_factory,
    token,
    ):
    """
    Testa a listagem de todos os usuários.
    """
    # Cria 3 usuários no banco de dados para o teste
    user_factory.create_batch(size=3)
    
    response = client.get(
        "/users/",
        headers={'Authorization': f'Bearer {token}'},
        )
    
    assert response.status_code == 200
    users_list = response.json()
    assert len(users_list) == 4
    # Verifica se os campos estão corretos no primeiro usuário da lista
    assert "username" in users_list[0]
    assert "password" not in users_list[0]

@pytest.mark.users
def test_get_user_by_id(
    client: TestClient, 
    user_factory,
    token
    ):
    """
    Testa a busca de um usuário específico pelo ID.
    """
    # Cria um usuário para ser buscado
    user = user_factory.create()

    response = client.get(
        f"/users/{user.id}",
        headers={'Authorization': f'Bearer {token}'},
        )
    
    assert response.status_code == 200
    found_user = response.json()
    assert found_user["id"] == user.id
    assert found_user["username"] == user.username

@pytest.mark.users
def test_get_user_by_id_not_found(
    client: TestClient, 
    token
    ):
    """
    Testa a busca por um usuário com um ID que não existe.
    """
    response = client.get(
        "/users/999",
        headers={'Authorization': f'Bearer {token}'},
        ) # Um ID que provavelmente não existe
    
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]

def test_update_user(
        client: TestClient, 
        user,
        token
        ):
    """
    Testa a atualização bem-sucedida de um usuário.
    """
    update_data = {"username": "new_username"}
    
    response = client.put(
        f"/users/{user.id}", 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'},
        )
    
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["username"] == "new_username"
    assert updated_user["email"] == user.email # O e-mail não deve ter mudado

def test_update_user_unauthozied(
        client: TestClient, 
        session: Session,
        ):
    """
    Testa a atualização de um usuário que não está logado.
    """
    update_data = {"username": "new_username"}
    response = client.put(
        "/users/999", 
        json=update_data,
        )
    
    assert response.status_code == 401

def test_delete_user(
    client: TestClient, 
    user_factory, 
    token
    ):
    """
    Testa a exclusão bem-sucedida de um usuário.
    """
    user = user_factory()
    
    # Deleta o usuário
    response_delete = client.delete(
        f"/users/{user.id}",
        headers={'Authorization': f'Bearer {token}'},
        )
    assert response_delete.status_code == 204 # No Content
    
    # Tenta buscar o usuário deletado para confirmar
    response_get = client.get(f"/users/{user.id}")
    assert response_get.status_code == 404

def test_delete_user_not_found(client: TestClient, session: Session):
    """
    Testa a exclusão de um usuário que não existe.
    """
    response = client.delete(
        "/users/999"
        )
    
    assert response.status_code == 401
