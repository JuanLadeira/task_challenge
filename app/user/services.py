from typing import List, Annotated, Optional

from fastapi import Depends
from sqlmodel import select

from app.auth.security import get_password_hash
from app.db import DBSession
from app.user.models import User
from app.user.schemas import UserCreate, UserUpdate


class UserService:
    """
    Esta classe encapsula a lógica de negócio para manipulação de usuários.
    Todas as interações com o banco de dados relacionadas a usuários devem passar por aqui.
    """

    def __init__(self, session: DBSession):
        """
        Inicializa o serviço com uma sessão de banco de dados injetada.

        Args:
            session: Uma sessão do SQLModel para interagir com o banco de dados.
        """
        self.session = session
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário pelo seu ID.
        Retorna o usuário se encontrado, ou None se não existir.
        
        Args:
            user_id: O ID do usuário a ser buscado.

        Returns:
            Um objeto User se encontrado, ou None se não existir.
        """
        user = self.session.get(User, user_id)
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Busca um usuário pelo nome de usuário.
        Retorna o usuário se encontrado, ou None se não existir.
        """
        user = self.session.exec(
            select(User).where(User.username == username)
        ).first()
        return user

    def get_all_users(self) -> List[User]:
        """Busca todos os usuários, ordenados por ID."""
        users = self.session.exec(select(User).order_by(User.id)).all()
        return users

    def create_user(self, user_data: UserCreate) -> User:
        """
        Cria um novo usuário a partir dos dados do schema UserCreate.

        Args:
            user_data: Um objeto UserCreate com os dados do novo usuário.

        Returns:
            O objeto do usuário recém-criado.
        """
        # Cria um dicionário com os dados do schema, excluindo a senha para tratá-la separadamente.
        user_dict = user_data.model_dump(exclude={"password"})
        
        # Aplica o hash na senha antes de armazená-la.
        hashed_password = get_password_hash(user_data.password)
        
        # Cria a instância do modelo User com os dados e a senha hasheada.
        db_user = User(**user_dict, password=hashed_password)
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Atualiza um usuário existente a partir dos dados do schema UserUpdate.

        Args:
            user_id: O ID do usuário a ser atualizado.
            user_data: Um objeto UserUpdate com os campos a serem atualizados.

        Returns:
            O objeto do usuário atualizado, ou None se não for encontrado.
        """
        # Busca o usuário no banco de dados.
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None

        # Obtém um dicionário com apenas os campos que foram enviados na requisição.
        update_data = user_data.model_dump(exclude_unset=True)

        # Trata a atualização da senha separadamente para aplicar o hash.
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password

        # Atualiza os campos do objeto do banco de dados.
        for key, value in update_data.items():
            if value:
                setattr(db_user, key, value)

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete_user_by_id(self, user_id: int) -> bool:
        """
        Deleta um usuário pelo seu ID.
        Retorna True se o usuário foi deletado, False caso contrário.
        """
        user = self.session.get(User, user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False


def get_user_service(session: DBSession) -> UserService:
    """
    Cria e retorna uma instância do UserService com a sessão
    de banco de dados injetada.
    """
    return UserService(session)


# Dependência para ser usada nos endpoints da API.
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
