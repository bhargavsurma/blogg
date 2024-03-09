from curses.ascii import HT
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status,HTTPException,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.params import Depends
from typing import List, Optional


router = APIRouter(
    #add prefix to all paths
    prefix="/posts",
    tags=['Posts'] #Used to group all routes together in swaggerUI documentation for better readability
)

#Get All Posts based on limit set by user
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search : Optional[str] = "" ):
    #psycopg2.cursor.execute("""SELECT * FROM posts""")
    #posts = psycopg2.cursor.fetchall()
    #post_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    results_query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    results = results_query.all()
    #posts = post_query.all()
    return results

#Create post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    #psycopg2.cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    #new_post = psycopg2.cursor.fetchone()
    #conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #current_usr.id is extracted from JWT token and added to json before inserting into the database
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    db.add(new_post) #Insert new post to the database
    db.commit() #Commit those changes
    db.refresh(new_post) #Return the post we inserted in this session

    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #psycopg2.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    #post = psycopg2.cursor.fetchone()
    
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post
 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # psycopg2.cursor.execute("""DELETE FROM posts WHERE id = %s""", (id,))
    # rows_deleted = psycopg2.cursor.rowcount
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested option")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # psycopg2.cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    # updated_post = psycopg2.cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested option")

    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()