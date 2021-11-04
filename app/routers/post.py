from .. import models,utils,oAuth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..schemas import *
from pydantic import BaseModel
from typing import Optional,List


router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get("/",response_model=List[PostResponse])
def get_post(db: Session = Depends(get_db),current_user : UserResponse = Depends(oAuth2.get_current_user),
             limit:int = 10,skip:int = 0,search:Optional[str] = ''):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                models.Post.id == models.Vote.post_id,isouter = True).group_by(models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=PostSchema)
def create_post(post: PostCreate,db: Session = Depends(get_db),
                current_user : UserResponse = Depends(oAuth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=PostResponse)
def get_post(id:int,response: Response,db: Session = Depends(get_db),current_user : UserResponse = Depends(oAuth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = (%s)",str(id))
    # post = cursor.fetchone()
    
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                models.Post.id == models.Vote.post_id,isouter = True).group_by(
                    models.Post.id).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session = Depends(get_db),current_user : UserResponse = Depends(oAuth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str((id)))
    # deleted = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist")
    if current_user.id != post.owner_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=PostSchema)
def update_posts(id:int,post:PostCreate,db: Session = Depends(get_db),current_user : UserResponse = Depends(oAuth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str((id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    db_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    db_post = db_post_query.first()
    
    if db_post == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                    detail=f"Post with id: {id} does not exist")
    if current_user.id != db_post.owner_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")

    db_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = db_post_query.first()
    return updated_post
