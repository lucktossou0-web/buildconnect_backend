from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_user
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

# --- GESTION DU PROFIL ---

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
    for var, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, var, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

# --- RÉALISATIONS ---

@router.post("/me/projects", response_model=schemas.ProjectOut)
def add_project(
        project_in: schemas.ProjectCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.UserRole.CLIENT:
        raise HTTPException(status_code=403, detail="Interdit aux clients")
    new_project = models.Project(**project_in.dict(), user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# --- MODÈLE ÉCONOMIQUE : PAIEMENTS ---

@router.post("/me/pay", response_model=schemas.PaymentOut)
def submit_payment_proof(
        payment_in: schemas.PaymentCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    new_pay = models.Payment(
        user_id=current_user.id,
        screenshot_url=payment_in.screenshot_url,
        status="pending"
    )
    current_user.has_pending_payment = True
    db.add(new_pay)
    db.commit()
    db.refresh(new_pay)
    return new_pay

# --- ADMINISTRATION ---

@router.get("/admin/all", response_model=List[schemas.UserOut])
def admin_get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin: raise HTTPException(status_code=403)
    return db.query(models.User).all()

@router.get("/admin/payments", response_model=List[schemas.PaymentOut])
def admin_get_pending_payments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin: raise HTTPException(status_code=403)
    return db.query(models.Payment).filter(models.Payment.status == "pending").all()

@router.post("/admin/payments/{payment_id}/approve")
def admin_approve_payment(payment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin: raise HTTPException(status_code=403)

    pay = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    user = db.query(models.User).filter(models.User.id == pay.user_id).first()

    pay.status = "approved"
    user.is_subscribed = True
    user.has_pending_payment = False

    # Calcul de la nouvelle date de fin (+30 jours)
    start_date = user.subscription_end if (user.subscription_end and user.subscription_end > datetime.now()) else datetime.now()
    user.subscription_end = start_date + timedelta(days=30)

    # Notification automatique par message interne
    notif = models.Message(
        sender_id=current_user.id,
        receiver_id=user.id,
        content=f"NOTIF : Votre paiement de 500 FCFA a été validé. Votre profil est actif jusqu'au {user.subscription_end.strftime('%d/%m/%Y')}."
    )
    db.add(notif)
    db.commit()
    return {"status": "success"}

@router.post("/admin/toggle-status/{user_id}")
def admin_toggle_user_active(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin: raise HTTPException(status_code=403)
    target = db.query(models.User).filter(models.User.id == user_id).first()
    target.is_active = not target.is_active
    db.commit()
    return {"is_active": target.is_active}