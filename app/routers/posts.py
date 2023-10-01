from .. import models, schemas # the '..' means up one directoy from current directory
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db #..database means database.py file in current directory
from .. import oauth2
#router = APIRouter()#create router object, and replace the @app to @router

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']) #since evey single route in this file starts with '/posts' 
                                        #we can just add the rpefix here so we dont't need to keep copying it in each request
                    #the tags parameter above helps in organizing the api documentation by organizing it into groups based on the tags provided so its easier to read the documentation
                    

@router.get("/", response_model=List[schemas.Post]) #to use the response model in this case (respone_model=List[schemas.Post]), need to import List from Typing or else will give error as it will try to convert multiple posts into one post format
# @router.get("/", response_model=List[schemas.PostOut]) #the above line does validation, this line skips the validation
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ""): #limit parameter is how many posts user wants to retrieve, the default is set to 10. skip parameter allows how many posts you want to skip.
    #skip can be used for pagenation: ir. if a page shows 10 results per page, to go to page 2, you would skip the first 10 results, to go to page 3, you would skip first 20 results and so on 
    
    #posts = db.query(models.Post).all()
    #to use the limit the query parameter limit needs to added to the url: {{URL}}posts?limit=5
    #to use the skip and limit parameters need to add to url: {{URL}}posts?limit=5&skip=2 .. this will skip the first 2 results and display the next 5,
    #to add more prameters, just use the & symbol

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #offset allows the skipping of first n search results 
        #from above, filter(models.Post.title.contains(search)) this will filter the results from search, them skip the numbers of posts defined by skip, and them limit the number of posts in limit
    #url for search: {{URL}}posts?limit=5&skip=2&search=post3
    #url for search with multiple words(ie spaces between words), use %20 to represt the space: {{URL}}posts?limit=5&skip=2&search=new%20post3 .. this will search for "new post3" 
    
    #the below query does a left join group by and count operation on the two tables
    #this is how to build acomplex query
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
    return posts #there is an issue with PostOut in schema file so can't return the results var 


# #if you want the user to only be able to get their own posts when they are logged in do this
# @router.get("/", response_model=List[schemas.Post]) #to use the response model in this case (respone_model=List[schemas.Post]), need to import List from Typing or else will give error as it will try to convert multiple posts into one post format
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
#     return posts 


#post request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #response_model=schemas.Post uses this class for the response from api
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #in this new_post is the variable, Post is calling the class Post which is doing the validation 
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)#this works but what if we had more fields to unpack? 
    #since post is a python dictionary, we can unpack all the fields it has by doing **post.dict()
    print(current_user.email)

    new_post = models.Post(owner_id=current_user.id, **post.dict()) #**will automatically unpack all the fields inside the post dictionary

    db.add(new_post)#add new post to db
    db.commit() #save the changes to the database
    db.refresh(new_post)#retrieve the new post we just created and store it back into the new_post variable so we can see see the changes in the database
    return new_post

#get post by id
@router.get("/{id}", response_model=schemas.Post) #id field represents a path parameter
#@router.get("/{id}", response_model=schemas.PostOut) #use for inluding votes, but giving internal server error
def get_post(id: int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #id:int will validate that id is int and will try to convert if it is possible, else will return error
    post = db.query(models.Post).filter(models.Post.id == id).first()#.first will find the first match and return that, if using .all() it would keep searching until everything is searched.
                                                                    #in this case we know id's are unique so don't need to search after we have a found a match
    
    
    #there is an issue with PostOut in schema file so can't return the results var 

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    
    
    if not post: #check if status code is found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"post with id: {id} was not found.")
    return  post


# #if you want user to only be able to get their own post
# @router.get("/{id}", response_model=schemas.Post) #id field represents a path parameter
# def get_post(id: int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #id:int will validate that id is int and will try to convert if it is possible, else will return error
#     post = db.query(models.Post).filter(models.Post.id == id).first()#.first will find the first match and return that, if using .all() it would keep searching until everything is searched.
#                                                                     #in this case we know id's are unique so don't need to search after we have a found a match
#     if not post: #check if status code is found
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail = f"post with id: {id} was not found.")
    
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


#     return  post


#delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False) #this synchronizing startagy is from sql alchamy documentation
                                            #they state its the most effieicnt and reliable, there are other available as well to look at under session basics
    db.commit() #commits the changes
    
    #when deleteing something, API does not want to send anything back, so there is no response
    #sent, back. the below return statment is just so there are no errors in code
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post with id
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)#setup query to find the post with the specific id
    post = post_query.first()#grab that specific post from the db

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    #the update function take a dictionary and update strategy(synchronize session)
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()