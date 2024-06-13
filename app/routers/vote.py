from fastapi import status, Depends, HTTPException, APIRouter
from app.oauth2 import get_current_user
from ..schemas import Vote, UserOut
from ..database import Session, get_db
from  .. import models

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.vote_status == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post with id {vote.post_id} has already been voted on")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "Vote scuccessfully added"
        }
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} has not been voted on")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Vote successfully deleted"
        }

