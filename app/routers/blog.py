from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from ..models import Blog, User, BlogCreate
from ..auth.dependencies import get_current_user
from app.rate_limit import limiter
from ..database import get_session

router = APIRouter(prefix="/blogs", tags=["Blogs"])


# Create blog
@router.post("/", response_model=Blog)
@limiter.limit("10/minute")
def create_blog(request: Request, blog: BlogCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    try:
        print(blog)
        db_blog = Blog(title=blog.title, content=blog.content)
        session.add(db_blog)
        session.commit()
        session.refresh(db_blog)
        return db_blog
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


# Update blog
@router.put("/{blog_id}", response_model=Blog)
@limiter.limit("10/minute")
def update_blog(request: Request, blog_id: int, updated: BlogCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = updated.title
    blog.content = updated.content
    session.commit()
    session.refresh(blog)
    return blog

# Delete blog
@router.delete("/{blog_id}")
@limiter.limit("10/minute")
def delete_blog(request: Request, blog_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return {"message": "Blog deleted"}
