from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..models import Blog
from ..database import get_session

router = APIRouter(prefix="/blogs", tags=["Blogs"])


# Create blog
@router.post("/", response_model=Blog)
def create_blog(blog: Blog, session: Session = Depends(get_session)):
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
def get_blogs(session: Session = Depends(get_session)):
    return session.exec(select(Blog)).all()


# Get single blog
@router.get("/{blog_id}", response_model=Blog)
def get_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog