from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from typing import List

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def read_user_me(current_username: str, db: Session = Depends(get_db)):
    # Note : Dans une version finale, on utiliserait un token JWT pour extraire le username
    user = db.query(models.User).filter(models.User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Professionnel non trouvé")
    return user

@router.patch("/me", response_model=schemas.UserOut)
def update_user_me(user_update: schemas.UserCreate, current_username: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == current_username).first()
    for var, value in vars(user_update).items():
        if value is not None:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user