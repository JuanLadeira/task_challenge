
from app.logger import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.todo import ui
from app.todo import router

## Subscribers
import app.todo.subscribers

from app.events import register_sqlalchemy_listeners, remove_sqlalchemy_listeners

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando o processo de criação do banco de dados e tabelas...")
    create_db_and_tables()

    logger.info("Iniciando a aplicação FastAPI...")
    logger.info("Registrando listeners do SQLAlchemy...")
    register_sqlalchemy_listeners()
    yield
    logger.info("Encerrando a aplicação FastAPI...")
    logger.info("Removendo listeners do SQLAlchemy...")
    remove_sqlalchemy_listeners()



app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(ui.router)
app.include_router(router.router)
