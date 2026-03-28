from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .database import engine
from .routers import blog

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "https://blog-frontend-react1.vercel.app"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SQLModel.metadata.create_all(engine)

app.include_router(blog.router)