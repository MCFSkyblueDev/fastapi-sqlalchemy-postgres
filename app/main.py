from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import users, items

app = FastAPI()

# UPLOAD_FILE=Path("uploads")
# UPLOAD_FILE.mkdir(parents=True, exist_ok=True)
app.mount("/upload", StaticFiles(directory="uploads"), name="upload")


app.include_router(users.user_router, prefix="/user", tags=["Users"])
app.include_router(items.item_router, prefix="/item", tags=["Items"])