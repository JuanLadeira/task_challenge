from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

from app.db import DBSession
from app.models import Todo
from app.services import TodoServiceDep
from app.schemas import TodoCreate, TodoUpdate


# --- Configuração do Router para a API REST ---
# É uma boa prática usar um prefixo para a API, como '/api/v1'
router = APIRouter(
    prefix="/api/todos",
    tags=["API REST de Tarefas"],
    responses={404: {"description": "Não encontrado"}}
)

# --- Endpoints da API REST ---

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED, summary="Criar uma nova tarefa")
def create_new_todo(
    todo_data: TodoCreate,
    service: TodoServiceDep  # Usando o alias para a dependência
):
    """
    Cria uma nova tarefa e a armazena no banco de dados.
    - **Corpo da Requisição**: Um JSON com o campo `content`.
    - **Retorna**: O objeto completo da tarefa criada.
    """
    return service.create_todo(content=todo_data.content)

@router.get("/", response_model=List[Todo], summary="Listar todas as tarefas")
def get_all_todos(service: TodoServiceDep): # Usando o alias para a dependência
    """
    Busca e retorna uma lista de todas as tarefas existentes.
    """
    return service.get_all_todos()

@router.get("/{todo_id}", response_model=Todo, summary="Buscar uma tarefa por ID")
def get_todo_by_id(
    todo_id: int,
    service: TodoServiceDep # Usando o alias para a dependência
):
    """
    Busca e retorna uma única tarefa pelo seu ID.
    Retorna um erro 404 se a tarefa não for encontrada.
    """
    # Para a API REST, é melhor buscar o todo aqui para poder retornar 404.
    # A camada de serviço poderia ser adaptada para isso.
    db_todo = service.session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_todo

@router.put("/{todo_id}", response_model=Todo, summary="Atualizar uma tarefa")
def update_existing_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    service: TodoServiceDep # Usando o alias para a dependência
):
    """
    Atualiza uma tarefa existente.
    - **Corpo da Requisição**: Um JSON com os campos a serem atualizados (`content` e/ou `completed`).
    - **Retorna**: O objeto da tarefa atualizada.
    """
    db_todo = service.session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # Pega os dados do Pydantic model e atualiza o objeto do SQLModel
    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    service.session.add(db_todo)
    service.session.commit()
    service.session.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletar uma tarefa")
def delete_existing_todo(
    todo_id: int,
    service: TodoServiceDep # Usando o alias para a dependência
):
    """
    Deleta uma tarefa específica pelo seu ID.
    Não retorna conteúdo em caso de sucesso.
    """
    was_deleted = service.delete_todo_by_id(todo_id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    # Nenhum retorno é necessário para o status 204
