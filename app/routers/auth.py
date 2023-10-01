from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm =Depends(), db: Session = Depends(database.get_db)):
            #in the above lineuser_credentials:OAuth2PasswordRequestForm =Depends(), this will make sure fastapi gets the credentials for the user before procedeing
            #user_credentials will only contain username and password in dict format
            #now in the request, the username and password needs to provided as form-data in the body of the request not as raw JSON , or else it will give error
                #in the form data: key: username Value: the username, key:password, value actual password

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    #verify correct password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    #create token
    access_token = oauth2.create_access_token(data={"user_id":user.id}) #here data is what you want to add to encode, you can choose anyhting, in this case we chose just the user id, 
                                                                #for example you can provide the scope of the user, admin, manager,etc. 

    #return token
    return{"access_token" : access_token, "token_type": "bearer"} 




