import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings 
#Create a database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

#Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Create a SessionLocal class
#Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
#But once we create an instance of the SessionLocal class, this instance will be the actual database session.
#We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
#We will use Session (the one imported from SQLAlchemy) later.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a Base class
#Now we will use the function declarative_base() that returns a class.
#Later we will inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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





