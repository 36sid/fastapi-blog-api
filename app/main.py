from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import blog

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(blog.router)