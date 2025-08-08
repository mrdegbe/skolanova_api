# app/core/dependencies.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_tenant_scoped_session

# from app.models.tenant import Tenant

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Database session dependency
def get_db(request: Request) -> Generator[Session, None, None]:
    db = getattr(request.state, "db", None)
    if db is None:
        raise RuntimeError("Database session not initialized")
    try:
        yield db
    finally:
        pass  # session closed in middleware


# def get_db(request: Request) -> Generator[Session, None, None]:
#     tenant_id = getattr(request.state.tenant, "id", None)
#     db = get_tenant_scoped_session(tenant_id=tenant_id)
#     try:
#         yield db
#     finally:
#         db.close()


# Authenticated user dependency
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# def get_current_tenant(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     slug = request.state.tenant_slug
#     tenant = db.query(Tenant).filter(Tenant.slug == slug).first()

#     if not tenant:
#         raise HTTPException(status_code=404, detail="Tenant not found")

#     return tenant
