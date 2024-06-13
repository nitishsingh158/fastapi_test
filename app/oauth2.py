import jwt
from datetime import datetime, timedelta, timezone
from .schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from . import models
from .config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, ):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except jwt.PyJWTError:
        raise credential_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schema), db = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credential could not be verified",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception=credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

