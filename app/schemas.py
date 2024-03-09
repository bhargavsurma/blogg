from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


# Pydantic model for User Operations

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
#Following lines in Response model convert sqlalchemy model to Pydantic model
    class Config:
        from_attributes =  True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Pydantic model for Posts

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#Response model
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    
    #converts the result from database(ORM/SQLAlchemy Model) to dict(Pydantic Model)
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True

#Pydantic model for votes

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore


# Pydantic model for Authentication


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

    