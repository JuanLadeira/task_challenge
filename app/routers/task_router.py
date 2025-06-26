from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from typing import Annotated

from app.db import DBSession
from app.models import Todo

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/", response_class=HTMLResponse)
def read_root(request: Request, session: DBSession):
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@router.post("/todos", response_class=HTMLResponse)
def create_todo(
    request: Request, 
    session: DBSession,
    content: str = Form(...),
    ):
    todo = Todo(content=content)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos})

@router.put("/todos/{todo_id}", response_class=HTMLResponse)
def update_todo(request: Request, todo_id: int, session: DBSession):
    todo = session.get(Todo, todo_id)
    if todo:
        todo.completed = not todo.completed
        session.add(todo)
        session.commit()
        session.refresh(todo)
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos})

@router.delete("/todos/{todo_id}", response_class=HTMLResponse)
def delete_todo(request: Request, todo_id: int, session: DBSession):
    todo = session.get(Todo, todo_id)
    if todo:
        session.delete(todo)
        session.commit()
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos})
