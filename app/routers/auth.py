from multiprocessing.resource_tracker import ResourceTracker
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication']) 

@router.post("/login",response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):

    #OAuth2PasswordRequestForm fetches email as username
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
 
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    #return token
    return {"access_token": access_token, "token_type" : "bearer"}