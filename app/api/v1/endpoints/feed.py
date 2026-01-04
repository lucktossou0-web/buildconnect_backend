from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[schemas.UserOut])
def get_feed(role: Optional[models.UserRole] = None, db: Session = Depends(get_db)):
    # LOGIQUE : Pas de clients, PAS D'ADMINS, seulement les actifs et abonnés
    query = db.query(models.User).filter(
        models.User.role != models.UserRole.CLIENT,
        models.User.is_admin == False, # <-- CACHE L'ADMIN
        models.User.is_active == True,
        models.User.is_subscribed == True
    )

    if role:
        query = query.filter(models.User.role == role)

    return query.all()