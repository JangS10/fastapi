from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


#use this class to define the scema for the Post call, in this case, this class would validate taht 
#the title in the Post body is a string, and content is string as well.
#if there are any additional items in the Post Body then it will give error only if the content 
    #and title are not string or can't be converted to string, then it will also give an error
# you have the option to provide a default value in case user doesn't provide it, if a default value is given
    #then there will be no errors
class Post(BaseModel):
    title: str
    content: str
    published: bool = False #give a default value that will be used if none provided in body or request 
    #rating: Optional[int] = None # make this optional, so it only is used if it is provided in the body of request

#connection to postgres DB
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database='fastapi', 
                                user='postgres', password = 'python11',
                                cursor_factory=RealDictCursor) #cursor_factory is used so the return from DB is a nice python dict
        cursor = conn.cursor() #used to execute SQL statements
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to DB failed!")
        print("Error: " , error)
        time.sleep(5)




my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "fav food", "content": "pizzaaa", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

@app.get("/") #this decorator turn the code below to act as an api, and turns the code to a path operation
                # in this case '/'. @app is referencing to the FastAPI() instance that was created
                # .get is the type of http method user should use, and ('/') is the path to the resource  
def root():

    return{"message": "My first API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()

    return {"data": posts} # my_posts is a dict, FastAPI will automatically serialize the dict and covert it to JSON



#post request
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: dict = Body(...)):  #payload: dict = Body(...) payload is variable name
                                                # dict is type of variable, in this case dictionary
                                                # Body(...) is import from FastAPI which retrieves the body of the post request
                                                #so this is basically getting the body of the post request and stroing it in payload varibale as a dictionary

    print (payload)
    #the below return send the conetent from 
    return {"new_post": f"title: {payload['title']}, content:{payload['content']}"}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post): #in this new_post is the variable, Post is calling the class Post which is doing the validation 
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() # saves the post to the database, if not done, database won't save

    return {"data": new_post}
    # for this post call now since validation is being done, if title or content are not given it will give error 
    # if anything other than title and content is given in the body of the post call, that part will be ignored unless it added to the Post class





@app.get("/posts/{id}") #id field represents a path parameter
def get_post(id: int): #id:int will validate that id is int and will try to convert if it is possible, else will return error
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()
    if not post: #check if status code is found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"post with id: {id} was not found.")
    return {"Post detail:": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    #when deleteing something, API does not want to send anything back, so there is no response
    #sent, back. the below return statment is just so there are no errors in code
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    return{'data' : updated_post}

3
