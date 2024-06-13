from fastapi import status, Depends, HTTPException, APIRouter
from typing import List, Optional

from sqlalchemy import func

from ..schemas import PostInDB, PostCreate, PostOut
from ..database import Session,  get_db
from  .. import models, oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session=Depends(get_db),
                     user: int = Depends(oauth2.get_current_user),
                     limit: int = 10, 
                     skip: int = 0,
                     search : Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
                .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
                .group_by(models.Post.id)\
                .filter(models.Post.title.contains(search))\
                .limit(limit)\
                .offset(skip)\
                .all()

    return posts

@router.get("/{id}", response_model=PostOut)
async def get_post(id:int, db=Depends(get_db),  user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
                .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
                .group_by(models.Post.id)\
                .filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=PostInDB)
async def create_posts(post: PostCreate, db=Depends(get_db), user = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", response_model=PostInDB)
def update_post(post: PostCreate, id: int, db=Depends(get_db),  user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first():
        update_post = post_query.first()
        if update_post.user_id == user.id:
            post_query.update(post.model_dump())
            db.commit()
            return post_query.first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db=Depends(get_db), user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        del_post = post.first()
        if del_post.user_id == user.id:
            post.delete(synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")


