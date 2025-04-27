
from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from app.decorators import check_role
from app.dependencies import get_current_user, get_item_service
from app.enums.roles import Role
from app.models.user import UserModel
from app.schemas.item import ItemCreate
from app.services.item import ItemService
from app.utils.file_manipulator import FileManipulator


class ItemRouter:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()
        
    def add_routes(self):
        @self.router.post("/create-item")
        @check_role([Role.USER])
        def create_item(item: ItemCreate,
                        user: UserModel = Depends(get_current_user),
                        item_service: ItemService = Depends(get_item_service)):
            return item_service.create_item(item, user.id)

        @self.router.post("/upload-file-content")
        def upload_file_content(file: Annotated[bytes, File()]):
            return {"file_size": len(file)}
            
        @self.router.post("/upload-file")
        def upload_file(file: UploadFile | None = None):
            return FileManipulator.save_file_to_local(file, "uploads")
        
item_router = ItemRouter().router