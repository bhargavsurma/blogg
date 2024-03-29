from datetime import datetime, timedelta
from fastapi.params import Depends
from fastapi import status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from httpx import head
from jose import JWTError, jwt
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

#name of the login end poit should be provided
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Following 3 information will be requried to be supplied in JWT token
#SECRET_KEY
#Algorithm
#Expiration Time for token

# to get a random string run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # First: everything going into the token, Second: Secret Key, Third: Algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise cred_exception
        
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise cred_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", 
                                   headers={"WWW-Authenticate":"Bearer"})
    

    token = verify_access_token(token, cred_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user