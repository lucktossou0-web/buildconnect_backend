from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core import security

# --- INITIALISATION DU ROUTER (Ligne manquante corrigée) ---
router = APIRouter()

@router.post("/register", response_model=schemas.Token)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Vérifier si l'email existe déjà
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    # 2. Vérifier si le pseudo existe déjà
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Ce pseudo est déjà pris")

    # 3. Préparation des données (logique de nettoyage selon le rôle)
    user_args = {
        "username": user_in.username,
        "email": user_in.email,
        "hashed_password": security.get_password_hash(user_in.password),
        "role": user_in.role,
        "city": user_in.city
    }

    if user_in.role == models.UserRole.PRESTATAIRE:
        user_args["specialty"] = user_in.specialty
        user_args["category"] = user_in.specialty
    elif user_in.role == models.UserRole.FOURNISSEUR:
        user_args["shop_name"] = user_in.shop_name
        user_args["category"] = "Matériaux"

    new_user = models.User(**user_args)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        print(f"Erreur DB: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création du compte")

    # 4. Génération du Token
    token = security.create_access_token(data={"sub": new_user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": new_user.username,
        "role": new_user.role,
        "user_id": new_user.id,
        "is_admin": new_user.is_admin
    }


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    # Vérification identifiants
    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    # Vérification si le compte est banni
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Ce compte a été banni par l'administrateur")

    # Génération du Token
    token = security.create_access_token(data={"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
        "user_id": user.id,
        "is_admin": user.is_admin
    }