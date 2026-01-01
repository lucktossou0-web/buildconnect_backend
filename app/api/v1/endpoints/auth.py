from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core import security

router = APIRouter()


@router.post("/register", response_model=schemas.Token)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Vérifier si l'utilisateur existe déjà
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # 2. Logique de nettoyage selon le rôle
    # On prépare les arguments de base
    user_args = {
        "username": user_in.username,
        "email": user_in.email,
        "hashed_password": security.get_password_hash(user_in.password),
        "role": user_in.role,
        "city": user_in.city
    }

    # On ajoute les champs SI ET SEULEMENT SI le rôle correspond
    if user_in.role == models.UserRole.PRESTATAIRE:
        user_args["specialty"] = user_in.specialty
        user_args["category"] = user_in.specialty
    elif user_in.role == models.UserRole.FOURNISSEUR:
        user_args["shop_name"] = user_in.shop_name
        user_args["category"] = "Matériaux"
    # Si c'est un CLIENT, specialty et shop_name resteront NULL en base de données.

    new_user = models.User(**user_args)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = security.create_access_token(data={"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer", "username": new_user.username, "role": new_user.role}


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):  # Utilise UserLogin ici
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        # 401 est plus standard pour une erreur d'auth que 403
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = security.create_access_token(data={"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }