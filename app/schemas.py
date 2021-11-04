from pydantic import BaseModel,EmailStr,ValidationError,validator
from datetime import datetime
from typing import  Optional


class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    email:EmailStr
    id:str
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post:PostSchema
    votes: int
    class Config:
        orm_mode = True    

class Vote(BaseModel):
    post_id: int
    dir: int
    
    @validator('dir')
    def dir_check(cls,dir):
        if dir not in (0,1):
            raise ValueError("dir Should be either 1 or 0")
        return dir
    
    