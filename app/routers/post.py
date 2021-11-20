from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts_db = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    post_db = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    return post_db


@router.get("/{post_id}", response_model=schemas.PostVote)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oauth2.get_current_user),
             limit: int = 10):

    # post_db = db.query(models.Post).filter(models.Post.id == post_id).first()

    post_db = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")). \
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id). \
        filter(models.Post.id == post_id).first()

    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")
    return post_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
