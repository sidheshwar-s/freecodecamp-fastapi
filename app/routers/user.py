from .. import models,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from pydantic import BaseModel
from typing import Optional,List

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    
    # hash the password for security
    user.password = utils.hash(user.password)
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except : 
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Email address: {user.email} already exist")

@router.get("/{id}",response_model=UserResponse)
def get_user(id:int,db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} does not exist")
    return user
    
    