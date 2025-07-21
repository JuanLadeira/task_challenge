from sqlmodel import SQLModel


class Token(SQLModel):
    acess_token: str
    token_type: str
