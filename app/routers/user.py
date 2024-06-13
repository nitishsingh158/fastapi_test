
from fastapi import status, Depends, HTTPException, APIRouter


from ..schemas import UserCreate, UserOut
from ..database import Session, get_db
from  .. import models
from ..utils import get_hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db=Depends(get_db)):
    user.password = get_hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserOut)
async def get_user(id: int, db=Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id).first()
    if user_query:
        return user_query
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found. ")