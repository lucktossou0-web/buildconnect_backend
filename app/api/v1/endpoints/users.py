from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_user
from typing import List

router = APIRouter()

# --- ROUTES UTILISATEURS STANDARDS ---

@router.get("/me", response_model=schemas.UserOut)
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.patch("/me", response_model=schemas.UserOut)
def update_user_me(
        user_update: schemas.UserUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    # Sécurité : Un client ne peut pas modifier certains champs complexes si tu le décides
    # Ici on permet la bio/phone/city pour tout le monde
    for var, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, var, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/projects", response_model=schemas.ProjectOut)
def add_project(
        project_in: schemas.ProjectCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    # RÉSERVÉ AUX PROS ET FOURNISSEURS
    if current_user.role == models.UserRole.CLIENT:
        raise HTTPException(status_code=403, detail="Les clients ne peuvent pas ajouter de réalisations")

    new_project = models.Project(**project_in.dict(), user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# --- ROUTES ADMINISTRATION ---

@router.get("/admin/all", response_model=List[schemas.UserOut])
def get_all_users_admin(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs")
    return db.query(models.User).all()

@router.post("/admin/toggle-status/{user_id}")
def toggle_user_active_status(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action interdite")

    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    target_user.is_active = not target_user.is_active
    db.commit()
    return {"status": "success", "is_active": target_user.is_active}