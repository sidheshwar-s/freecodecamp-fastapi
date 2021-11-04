from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,database,models,oAuth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote',tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user:schemas.UserResponse = Depends(oAuth2.get_current_user)):
    
    db_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not db_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id = {vote.post_id} is not found")
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    db_vote = vote_query.first()
    if vote.dir == 1: 
        if db_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted the post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else: 
        if not db_vote: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully removed vote "}
        