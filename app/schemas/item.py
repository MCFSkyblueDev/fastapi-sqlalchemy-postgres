from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ItemBase(BaseModel):
    name: Annotated[str,Field(..., max_length=256)]
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    owner_id: Annotated[int,Field(...)] 

    class Config:
        from_attributes = True  
