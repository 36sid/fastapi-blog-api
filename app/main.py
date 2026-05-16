from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from .rate_limit import limiter
from sqlmodel import SQLModel
from typing import cast, Callable
from .database import engine
from .routers import blog, auth

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://blog-frontend-react1.vercel.app"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

SQLModel.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(auth.router)
