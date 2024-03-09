from os import error
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status,HTTPException, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user_exist_query = db.query(models.User).filter(models.User.email == user.email)
        existing_user = user_exist_query.first()
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Choose another email.")


        #hash the password  - user.password
        user.password = utils.hash(user.password)

        new_user = models.User(**user.model_dump())
        db.add(new_user) 
        db.commit()
        db.refresh(new_user)

        return new_user
    except error as e:
        print(e)

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user