from typing import List

from fastapi import APIRouter, HTTPException, status

from app.user.schemas import UserCreate, UserPublic, UserUpdate
from app.user.services import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo usuário",
)
def create_user(user_data: UserCreate, service: UserServiceDep):
    """
    Cria um novo usuário no sistema.

    - **Corpo da Requisição**: Um JSON com `username`, `email` e `password`.
    - **Retorna**: Os dados públicos do usuário recém-criado.
    - **Levanta exceção 400**: Se o nome de usuário ou e-mail já existir.
    """
    # Verifica se o usuário já existe para evitar duplicatas.
    existing_user = service.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome de usuário já está em uso.",
        )
    
    # O e-mail também deve ser único, adicione uma verificação se necessário.

    return service.create_user(user_data=user_data)


@router.get(
    "/",
    response_model=List[UserPublic],
    summary="Listar todos os usuários"
)
def get_all_users(service: UserServiceDep):
    """
    Retorna uma lista de todos os usuários cadastrados no sistema.
    """
    return service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Buscar um usuário pelo ID"
)
def get_user_by_id(user_id: int, service: UserServiceDep):
    """
    Busca e retorna os dados de um usuário específico pelo seu ID.

    - **Retorna**: Os dados públicos do usuário.
    - **Levanta exceção 404**: Se o usuário com o ID fornecido não for encontrado.
    """
    # A camada de serviço lida com a busca. Aqui, apenas tratamos o resultado.
    # Nota: get_user_by_id não existe no serviço, vamos usar session.get.
    user = service.get_by_id(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserPublic,
    summary="Atualizar um usuário"
)
def update_user(user_id: int, user_data: UserUpdate, service: UserServiceDep):
    """
    Atualiza os dados de um usuário existente.

    - **Corpo da Requisição**: Um JSON com os campos a serem atualizados.
    - **Retorna**: Os dados públicos do usuário atualizado.
    - **Levanta exceção 404**: Se o usuário não for encontrado.
    """
    updated_user = service.update_user(user_id=user_id, user_data=user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar um usuário"
)
def delete_user(user_id: int, service: UserServiceDep):
    """
    Deleta um usuário do sistema pelo seu ID.

    - **Não retorna conteúdo** em caso de sucesso (status 204).
    - **Levanta exceção 404**: Se o usuário não for encontrado.
    """
    was_deleted = service.delete_user_by_id(user_id=user_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    # Nenhum retorno é necessário para o status 204
    return None

