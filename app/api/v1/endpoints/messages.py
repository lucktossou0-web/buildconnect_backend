from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_user
from typing import List

router = APIRouter()

# Route pour envoyer un message
@router.post("/", response_model=schemas.MessageOut)
def send_message(msg_in: schemas.MessageCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_msg = models.Message(
        sender_id=current_user.id,
        receiver_id=msg_in.receiver_id,
        content=msg_in.content
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# Route pour l'inbox (liste des gens avec qui on parle)
@router.get("/inbox", response_model=List[schemas.UserOut])
def get_inbox(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sent = db.query(models.Message.receiver_id).filter(models.Message.sender_id == current_user.id)
    received = db.query(models.Message.sender_id).filter(models.Message.receiver_id == current_user.id)
    ids = [r[0] for r in sent.union(received).all()]
    return db.query(models.User).filter(models.User.id.in_(ids)).all()

# CORRECTION : Route précise pour la conversation
@router.get("/conversation/{with_user_id}", response_model=List[schemas.MessageOut])
def get_conversation(with_user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == current_user.id, models.Message.receiver_id == with_user_id),
            and_(models.Message.sender_id == with_user_id, models.Message.receiver_id == current_user.id)
        )
    ).order_by(models.Message.created_at.asc()).all()