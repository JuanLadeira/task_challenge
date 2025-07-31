from typing import Annotated
from fastapi import Depends
from app.settings import Settings
from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(Settings().DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_session)]
