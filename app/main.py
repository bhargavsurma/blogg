from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .routers import post, user, auth, vote
from .database import engine, get_db

#set passlib default algorithm to bcrypt 

#Following line generate and run create statements for tables | sqlalchemy
#models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "XXXX API"}




