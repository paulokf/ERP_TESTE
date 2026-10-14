from typing import List, Optional
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.user import UserModel, UserRole

# Esquema padrão OAuth2 para documentação Swagger e rotas normais de API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def _get_user_from_raw_token(token: str, db: AsyncSession) -> UserModel:
    """Função utilitária interna para decodificar JWT e buscar o usuário ativo no banco."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas, token malformado ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: Optional[str] = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = await db.get(UserModel, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo ou não cadastrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserModel:
    """Extrai o usuário autenticado via cabeçalho Authorization: Bearer <token>."""
    return await _get_user_from_raw_token(token, db)


async def get_current_user_flexible(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> UserModel:
    """
    Autenticação flexível: aceita token via cabeçalho 'Authorization: Bearer <token>' 
    OU via Query Parameter '?token=...'. Essencial para carregar imagens/laudos 
    diretamente em tags <img> ou <iframe> sem disparar 401.
    """
    raw_token: Optional[str] = None

    if authorization and authorization.startswith("Bearer "):
        raw_token = authorization.split(" ")[1]
    elif token:
        raw_token = token

    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido no cabeçalho ou parâmetro.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_from_raw_token(raw_token, db)


class RequireRoles:
    """
    Injetor de dependência para controle de acesso por papéis (RBAC).
    Permite bypass automático para o perfil 'master'.
    
    Exemplo de uso:
        dependencies=[Depends(RequireRoles([UserRole.medico, UserRole.cirurgiao]))]
    """
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserModel = Depends(get_current_user)) -> UserModel:
        # Perfil 'master' possui acesso irrestrito
        if current_user.role == UserRole.master or current_user.role in self.allowed_roles:
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permissão negada. Requer um dos seguintes privilégios: {[r.value for r in self.allowed_roles]}"
        )

