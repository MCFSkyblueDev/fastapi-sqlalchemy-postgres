from app.config.config import Config
from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

from app.schemas.user import TokenData



SECRET_KEY = Config.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES


class JwtUtils:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        """Generate a JWT token with expiration."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str):
        """Decode and verify JWT token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str | None = payload.get("email")
            if email is None:
                raise credentials_exception
            return TokenData(access_token=token, token_type="bearer", email=email)
        except JWTError:
            raise credentials_exception