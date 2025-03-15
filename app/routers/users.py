from fastapi import APIRouter, Depends
from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user import UserService


class UserRouter:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()
        
    def add_routes(self):
        @self.router.post("/register", response_model=UserResponse)
        def register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
            return user_service.register(user)
        
        @self.router.post("/login")
        def login(user: UserLogin, user_service: UserService = Depends(get_user_service)):
            return user_service.login(user)

user_router = UserRouter().router

