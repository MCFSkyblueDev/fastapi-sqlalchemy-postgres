from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user import UserModel
from app.services.item import ItemService
from app.services.user import UserService
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from app.utils.jwt import JwtUtils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)
security = HTTPBearer()


def get_db():
    db : Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

def get_item_service(db: Session = Depends(get_db)):
    return ItemService(db)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        token_data = JwtUtils.decode_access_token(token)
        if token_data is None or token_data.email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # user = db.query(User).filter(User.email == token_data.email).first()
        result = db.execute(select(UserModel).filter(UserModel.email == token_data.email))
        user = result.scalars().first()  #result.scalars() extracts only the model objects from the query result.
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    