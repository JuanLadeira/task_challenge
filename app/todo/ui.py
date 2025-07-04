from typing import Annotated

from fastapi import APIRouter, Request, Form, Path, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.todo.services import TodoServiceDep
from app.todo.models import Todo
from app.todo.schemas import TodoUpdate


# Configuração do router e dos templates
router = APIRouter(
    tags=["Interface de Tarefas (HTMX)"],
    responses={404: {"description": "Não encontrado"}},
)
templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Busca a página HTML principal da aplicação",
)
def read_root(request: Request, service: TodoServiceDep):
    """
    Renderiza e retorna a página web completa (`base.html`).

    Este é o ponto de entrada da aplicação. Ele serve a página inicial que contém
    a estrutura completa, incluindo o formulário e a lista inicial de tarefas.
    As interações subsequentes (criar, atualizar, deletar) são feitas por outros
    endpoints que retornam fragmentos de HTML (parciais).
    """
    todos = service.get_all_todos()
    return templates.TemplateResponse("base.html", {"request": request, "todos": todos})


@router.post(
    "/ui/todos",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova tarefa e retorna a lista atualizada",
)
def create_todo(
    request: Request,
    service: TodoServiceDep,
    content: Annotated[
        str,
        Form(description="Conteúdo da tarefa a ser criada. Enviado como 'form data'."),
    ],
):
    """
    Cria uma nova tarefa a partir dos dados de um formulário.

    Este endpoint recebe dados no formato `application/x-www-form-urlencoded`.
    Após criar a tarefa no banco de dados, ele renderiza e retorna um **fragmento HTML**
    (`todos.html`) contendo toda a lista de tarefas atualizada. A interface (HTMX)
    substitui o conteúdo do elemento `#todos` por esta resposta.
    """
    todo = service.create_todo(content=content)
    if not todo:
        return HTMLResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="Erro ao criar a tarefa."
        )

    todos = service.get_all_todos()
    return templates.TemplateResponse(
        "todos.html", {"request": request, "todos": todos}
    )


@router.put(
    "/ui/todos/{todo_id}",
    response_class=HTMLResponse,
    summary="Atualiza o estado de uma tarefa",
)
def update_todo(
    request: Request,
    service: TodoServiceDep,
    todo_id: Annotated[
        int,
        Path(description="O ID da tarefa que terá seu estado 'completed' alternado."),
    ],
    todo_data: TodoUpdate = None, 
):
    """
    Alterna o estado de 'concluída' para uma tarefa específica.

    Este endpoint não espera um corpo na requisição. A ação é identificada pelo ID na URL.
    Após atualizar o estado da tarefa, ele retorna um **fragmento HTML** (`todos.html`)
    com a lista de tarefas atualizada, para ser usado pelo HTMX na substituição do conteúdo.
    """
    todo = service.update_todo(todo_id, todo_data)
    if not todo:
        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Tarefa não encontrada."
        )

    todos = service.get_all_todos()
    return templates.TemplateResponse(
        "todos.html", {"request": request, "todos": todos}
    )


@router.delete(
    "/ui/todos/{todo_id}",
    response_class=HTMLResponse,
    summary="Deleta uma tarefa específica",
)
def delete_todo(
    request: Request,
    service: TodoServiceDep,
    todo_id: Annotated[int, Path(description="O ID da tarefa a ser deletada.")],
):
    """
    Remove uma tarefa do banco de dados.

    Após deletar a tarefa identificada pelo ID na URL, este endpoint retorna um
    **fragmento HTML** (`todos.html`) com a lista de tarefas restante. Este
    fragmento é então usado pelo cliente (HTMX) para atualizar a interface.
    """
    todo = service.session.get(Todo, todo_id)
    if not todo:
        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Tarefa não encontrada."
        )

    service.delete_todo_by_id(todo_id)

    todos = service.get_all_todos()
    return templates.TemplateResponse(
        "todos.html", {"request": request, "todos": todos}
    )
