

from pydantic_settings import BaseSettings

#from pydantic_settings import BaseSettings 

#provide the environment variables that need to be set
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str = "localhost" #default value is localhost
    database_username: str 
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int

    #import the above settings from .env file
    class Config:
        env_file=".env"

#create instance of settings class for pydantic to read the environment vairables, perform the validations for datatype
settings = Settings()
#now you can access all the properties from Settings and use the environment variables
