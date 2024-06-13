from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models
from ..schemas import Token
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_user(user_credential: OAuth2PasswordRequestForm = Depends() , db=Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = create_access_token(data= {"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
