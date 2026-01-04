import sys
import os
from datetime import datetime, timedelta

# Permet d'importer le module 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models import models
from app.core.security import get_password_hash

def run_seed():
    db = SessionLocal()
    print("🚀 Démarrage du Smart Seed BuildConnect...")

    # On ne supprime que les tables temporaires si besoin,
    # mais on ne touche SURTOUT PAS à models.User.delete()

    expiry = datetime.now() + timedelta(days=365) # 1 an pour être tranquille en test

    users_data = [
        {
            "username": "ibrahim_arch",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Cotonou",
            "specialty": "Architecture & Design",
            "description": "Plans de villas modernes et suivi de chantier professionnel.",
            "avatar_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "sommet_quinc",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Porto-Novo",
            "shop_name": "Quincaillerie Le Sommet",
            "description": "Fer à béton, ciment Lafarge et outillage lourd.",
            "avatar_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "benin_carreaux",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Cotonou",
            "shop_name": "Showroom Carrelage",
            "description": "Importateur de marbre et grès cérame haute qualité.",
            "avatar_url": "https://images.unsplash.com/photo-1516156008625-3a9d6067fab5?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "moussa_macon",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Abomey-Calavi",
            "specialty": "Gros Oeuvre",
            "description": "Expert en fondations, dallage et élévation de murs.",
            "avatar_url": "https://images.unsplash.com/photo-1541888946425-d81bb19480c5?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "ets_lumiere",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Parakou",
            "specialty": "Électricité",
            "description": "Installations électriques industrielles et domotique.",
            "avatar_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "plomberie_benin",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Ouidah",
            "specialty": "Sanitaire & Plomberie",
            "description": "Dépannage 24/7 et installation de tuyauterie cuivre/PPR.",
            "avatar_url": "https://images.unsplash.com/photo-1585704032915-c3400ca1f963?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "bois_du_nord",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Djougou",
            "shop_name": "Menuiserie Bois Nord",
            "description": "Bois de charpente, contreplaqué et teck local.",
            "avatar_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "username": "elite_peinture",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Cotonou",
            "specialty": "Finition & Peinture",
            "description": "Peinture décorative, staff et enduits lisses.",
            "avatar_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=1000&auto=format&fit=crop"
        }
    ]

    for u in users_data:
        # ON VÉRIFIE SI L'UTILISATEUR EXISTE DÉJÀ
        existing_user = db.query(models.User).filter(models.User.username == u["username"]).first()

        if not existing_user:
            print(f"➕ Création de l'expert : {u['username']}")
            new_user = models.User(
                username=u["username"],
                email=f"{u['username']}@buildconnect.bj",
                hashed_password=get_password_hash("password123"),
                role=u["role"],
                city=u["city"],
                specialty=u.get("specialty"),
                shop_name=u.get("shop_name"),
                category=u.get("specialty") or "Matériaux",
                avatar_url=u["avatar_url"],
                is_subscribed=True, # Mock data toujours abonnée
                subscription_end=expiry,
                is_active=True,
                is_admin=False
            )
            db.add(new_user)
        else:
            # OPTIONNEL : Mettre à jour les infos si elles ont changé (photo, etc.)
            print(f"🔄 Mise à jour de l'expert : {u['username']}")
            existing_user.avatar_url = u["avatar_url"]
            existing_user.is_subscribed = True
            existing_user.subscription_end = expiry

    # GESTION DU COMPTE ADMIN PAR DÉFAUT
    default_admin = db.query(models.User).filter(models.User.username == "admin").first()
    if not default_admin:
        print("➕ Création du compte admin système (admin/admin123)")
        admin = models.User(
            username="admin",
            email="admin@buildconnect.bj",
            hashed_password=get_password_hash("admin123"),
            role=models.UserRole.PRESTATAIRE,
            city="Cotonou",
            is_admin=True,
            is_active=True,
            is_subscribed=True,
            subscription_end=expiry
        )
        db.add(admin)

    db.commit()
    print("\n✅ Seed terminé ! Tes comptes personnels sont préservés et les données de test sont à jour.")

if __name__ == "__main__":
    run_seed()