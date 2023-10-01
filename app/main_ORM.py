#Using Object Relational Mapper(ORM): sqlalchemy


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models  # the '.' means current directory
from .database import engine #.database means database.py file in current directory
from . routers import posts, users, auth, vote
from .config import settings

#the below line is not needed when using alembic
#all it does is tells sqlalchemy to run and create all the required tables
#since we have alembic this is not needed
#you can still keep it in as it wont break anything, all it will do is make the first alembic revision pointless as it has already created the initial tables that the models.py file specifies
#alembic will take over and auto generate any changes from here on out 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com"] #to allow all public access set to : ["*"]
#add middleware for CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,#allowed domains
    allow_credentials=True,
    allow_methods=["*"], #allowed HTTP methods, * means all are allowd
    allow_headers=["*"], #allowed headers, * all methods are allowed
)


app.include_router(posts.router) #will add all routes from post.py
app.include_router(users.router) #will add all routs from users.py
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #this decorator turn the code below to act as an api, and turns the code to a path operation
                # in this case '/'. @app is referencing to the FastAPI() instance that was created
                # .get is the type of http method user should use, and ('/') is the path to the resource  
def root():
    return{"message": "My first API"}




