from typing import Annotated

from fastapi import APIRouter, Request, Form, Path, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from app.todo.services import TodoServiceDep
from app.todo.models import Todo
from app.todo.schemas import TodoUpdate
from app.auth.auth_ui import get_current_user_from_cookie
from app.user.models import User

# Configuração do router e dos templates
router = APIRouter(
    tags=["Interface de Tarefas (HTMX)"],
    responses={404: {"description": "Não encontrado"}},
)
templates = Jinja2Templates(directory="app/templates")

UserDep = Annotated[User, Depends(get_current_user_from_cookie)]


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Busca a página HTML principal da aplicação",
)
def read_root(request: Request, service: TodoServiceDep, user: UserDep):
    """
    Renderiza a página de login se o usuário não estiver autenticado.
    Caso contrário, renderiza a página principal com a lista de tarefas.
    """
    if not user:
        return templates.TemplateResponse("login.html", {"request": request})

    todos = service.get_all_todos(user_id=user.id)
    return templates.TemplateResponse("base.html", {"request": request, "todos": todos, "user": user})


@router.post(
    "/ui/todos",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova tarefa e retorna a lista atualizada",
)
def create_todo(
    request: Request,
    service: TodoServiceDep,
    user: UserDep,
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
    if not user:
        return RedirectResponse(url="/ui/auth/login", status_code=status.HTTP_302_FOUND)

    todo = service.create_todo(content=content, user_id=user.id)
    if not todo:
        return HTMLResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="Erro ao criar a tarefa."
        )

    todos = service.get_all_todos(user_id=user.id)
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
    user: UserDep,
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
    if not user:
        return RedirectResponse(url="/ui/auth/login", status_code=status.HTTP_302_FOUND)

    todo = service.update_todo(todo_id, todo_data, user_id=user.id)
    if not todo:
        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Tarefa não encontrada."
        )

    todos = service.get_all_todos(user_id=user.id)
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
    user: UserDep,
    todo_id: Annotated[int, Path(description="O ID da tarefa a ser deletada.")],
):
    """
    Remove uma tarefa do banco de dados.

    Após deletar a tarefa identificada pelo ID na URL, este endpoint retorna um
    **fragmento HTML** (`todos.html`) com a lista de tarefas restante. Este
    fragmento é então usado pelo cliente (HTMX) para atualizar a interface.
    """
    if not user:
        return RedirectResponse(url="/ui/auth/login", status_code=status.HTTP_302_FOUND)

    todo = service.session.get(Todo, todo_id)
    if not todo or todo.user_id != user.id:
        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Tarefa não encontrada."
        )

    service.delete_todo_by_id(todo_id, user_id=user.id)

    todos = service.get_all_todos(user_id=user.id)
    return templates.TemplateResponse(
        "todos.html", {"request": request, "todos": todos}
    )