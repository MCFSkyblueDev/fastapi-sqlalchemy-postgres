from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.item import ItemModel
from app.schemas.item import ItemCreate


class ItemService:
    def __init__(self, db: Session):
        self.db = db
        
    def create_item(self, item : ItemCreate, owner_id : int):
        try:
            new_item = ItemModel(
                name=item.name, description=item.description, owner_id=owner_id
            )
            self.db.add(new_item)
            self.db.commit()
            self.db.refresh(new_item)
            print(new_item)
            return new_item
        except Exception as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )   