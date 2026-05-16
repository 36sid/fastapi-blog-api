from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from ..models import Blog, User
from ..auth.dependencies import get_current_user
from app.rate_limit import limiter
from ..database import get_session

router = APIRouter(prefix="/blogs", tags=["Blogs"])


# Create blog
@router.post("/", response_model=Blog)
@limiter.limit("10/minute")
def create_blog(request: Request, blog: Blog, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    try:
        print(blog)
        session.add(blog)
        session.commit()
        session.refresh(blog)
        return blog
    except Exception as e:
        print(f"Error creating blog: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Get all blogs
@router.get("/", response_model=list[Blog])
@limiter.limit("30/minute")
def get_blogs(request: Request, session: Session = Depends(get_session)):
    return session.exec(select(Blog)).all()


# Get single blog
@router.get("/{blog_id}", response_model=Blog)
@limiter.limit("30/minute")
def get_blog(request: Request, blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog