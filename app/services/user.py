from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.schemas.user import TokenData, UserCreate, UserLogin
from app.utils.hasher import Hasher
from app.utils.jwt import JwtUtils


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user: UserCreate):
        try:
            hash_password = Hasher.get_password_hash(user.password)
            new_user = UserModel(
                name=user.name, email=user.email, hashed_password=hash_password
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            print(new_user)
            return new_user
        except Exception as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )   
        
    def login(self, user: UserLogin):
        try:
            # db_user = self.db.query(UserModel).filter(UserModel.email == user.email)
            result = self.db.execute(select(UserModel).filter(UserModel.email == user.email))
            db_user = result.scalars().first()
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            if not Hasher.verify_password(user.password, db_user.hashed_password):
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
            access_token = JwtUtils.create_access_token(data={"email" : db_user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                )   
        
    
