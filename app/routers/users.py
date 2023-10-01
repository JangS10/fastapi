from .. import models, schemas, utils # the '..' means up one directoy from current directory
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db #.database means database.py file in current directory

#router = APIRouter() #create router object and replace @app to @router

router = APIRouter(prefix = "/users",
    tags=['Posts']) #since evey single route in this file starts with '/users' 
                                        #we can just add the rpefix here so we dont't need to keep copying it in each request
                                #the tags parameter above helps in organizing the api documentation by organizing it into groups based on the tags provided so its easier to read the documentation
                    

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
#response_model uses the UserOut Schema from schemas.py to return a response according to that defined schema
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db) ):

    #before creating the new user, hash the password in user.password
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password #update the user.password with the hashed password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id ==id).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details= f"User with id: {id} does not exist.")
    
    return user
