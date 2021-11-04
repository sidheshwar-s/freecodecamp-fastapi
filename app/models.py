from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, nullable = False)
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default='TRUE',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
    owner_id = Column(Integer(),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"
    
    email = Column(String,nullable = False,unique = True)
    password = Column(String,nullable = False)
    id = Column(Integer,primary_key = True,nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))

class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key = True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key = True)