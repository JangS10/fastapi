#Create SQLAlchemy models from the Base class

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Post(Base):
    #The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    __tablename__ = "posts"

# Create model attributes/columns¶
# Now create all the model (class) attributes.
# Each of these attributes represents a column in its corresponding database table.
# We use Column from SQLAlchemy as the default value.
# And we pass a SQLAlchemy class "type", as Integer, String, and Boolean, that defines the type in the database, as an argument.
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #this will display the post owner(user id) so all users know who creted the post.
    #this relationship is not a forien key and has no impact on the DB. it tells sqlalchamy to automatically 
    #fetch some piece of info based on the relationship.
    #this will automatically create a property for our post so when we retrieve a post it will return the owner property and fetch the user
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable=False)
    email = Column(String, nullable=False, unique=True) #email cant be null and must be unique(doesn't already exist in db)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# Create the relationships
# Now create the relationships.
# For this, we use relationship provided by SQLAlchemy ORM.
# This will become, more or less, a "magic" attribute that will contain the values from other tables related to this one.
    #items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)





