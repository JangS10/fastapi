from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#use this class to define the schema for the Post call, in this case, this class would validate taht 
#the title in the Post body is a string, and content is string as well.
#if there are any additional items in the Post Body then it will give error only if the content 
    #and title are not string or can't be converted to string, then it will also give an error
# you have the option to provide a default value in case user doesn't provide it, if a default value is given
    #then there will be no errors


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False 

class PostCreate(PostBase):
    #inherits PostBase
    pass 

class PostUpdate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    #need to add this for pydantic model since the Post will be a sql alchamy model not a dict and pydantic doens;t know how to work with those
    #so, this will tell it to convert sql alchmey model to pydantic model 
    class Config:
        orm_mode = True


class Post(PostBase): #response from api
    #inherits title, content and published from PostBase class, add the id and created at from this class
    id: int
    owner_id: int
    created_at: datetime
    
    #return a pydantic model with owner info, using the UserOut class, this UserOut class needs to be above this in the code, or else it will give error  
    owner: UserOut

    #need to add this for pydantic model since the Post will be a sql alchamy model not a dict and pydantic doens;t know how to work with those
    #so, this will tell it to convert sql alchmey model to pydantic model 
    class Config:
        orm_mode = True

#the below code broke the app.. video 10:26
class PostOut(PostBase):
    Post: Post #this gives internal server error, so copy the code from Post above
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr #imported form pydantic lib, verifies string is in email format
    password:str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]= None


class Vote(BaseModel):
    post_id: int
    dir:conint(le=1) #try to only allow a 0 or 1, this will also allow -1 if you find something that will only restric to 0 and 1, use that
    

