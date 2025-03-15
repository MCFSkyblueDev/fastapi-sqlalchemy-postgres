from pydantic import BaseModel, EmailStr, Field, StringConstraints, constr, model_validator
from typing import Annotated, Optional
from typing_extensions import Self


class UserProfileBase(BaseModel):
    bio: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: Annotated[str, Field(...)]
    email: Annotated[EmailStr, Field(...)]
    
class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(...)]
    password: str

class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(strict=True)]
    password_repeat: Annotated[str, StringConstraints(strict=True)]

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self
    

class UserResponse(UserBase):
    id: int
    profile: Optional[UserProfile] = None

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
