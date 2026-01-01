# buildconnect_backend/seed.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.db.session import SessionLocal
from app.models import models
from app.core.security import get_password_hash


def run_seed():
    db = SessionLocal()
    print("Nettoyage de la base...")
    db.query(models.Message).delete()
    db.query(models.User).delete()

    print("Création des profils avec photos professionnelles BTP...")

    users_data = [
        {
            "username": "ibrahim_arch",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Cotonou",
            "specialty": "Architecture & Design",
            "category": "Architecture",
            "description": "Expert en plans 3D et suivi de chantier pour villas de luxe.",
            "avatar_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=1000&auto=format&fit=crop",
            # Plan architcture
            "rating": 4.9
        },
        {
            "username": "sommet_quinc",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Porto-Novo",
            "shop_name": "Quincaillerie Le Sommet",
            "category": "Matériaux",
            "description": "Vente de fer à béton, ciment et outillage professionnel.",
            "avatar_url": "https://images.unsplash.com/photo-1581094288338-2314dddb7ecc?q=80&w=1000&auto=format&fit=crop",
            # Outils quincaillerie
            "rating": 4.7
        },
        {
            "username": "benin_carreaux",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Cotonou",
            "shop_name": "Bénin Carrelage",
            "category": "Revêtements",
            "description": "Showroom de carreaux marbrés et porcelaine importée.",
            "avatar_url": "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=1000&auto=format&fit=crop",
            # Expo carrelage
            "rating": 4.8
        },
        {
            "username": "moussa_macon",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Abomey-Calavi",
            "specialty": "Gros Oeuvre",
            "category": "Maçonnerie",
            "description": "Équipe spécialisée dans le coffrage et l'élévation de murs.",
            "avatar_url": "https://images.unsplash.com/photo-1541888946425-d81bb19480c5?q=80&w=1000&auto=format&fit=crop",
            # Mur de briques
            "rating": 4.5
        },
        {
            "username": "lumiere_ets",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Parakou",
            "specialty": "Électricité",
            "category": "Installation",
            "description": "Tableaux électriques complexes et domotique.",
            "avatar_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=1000&auto=format&fit=crop",
            # Câbles électriques
            "rating": 4.6
        },
        {
            "username": "sebastien_plomb",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Ouidah",
            "specialty": "Plomberie",
            "category": "Sanitaire",
            "description": "Installation de tuyauterie et équipements de salle de bain.",
            "avatar_url": "https://images.unsplash.com/photo-1585704032915-c3400ca1f963?q=80&w=1000&auto=format&fit=crop",
            # Tuyaux cuivre
            "rating": 4.7
        },
        {
            "username": "bois_du_nord",
            "role": models.UserRole.FOURNISSEUR,
            "city": "Djougou",
            "shop_name": "Bois du Nord",
            "category": "Menuiserie",
            "description": "Charpente, bois rouge et teck de première qualité.",
            "avatar_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?q=80&w=1000&auto=format&fit=crop",
            # Stock de bois
            "rating": 4.4
        },
        {
            "username": "elite_peinture",
            "role": models.UserRole.PRESTATAIRE,
            "city": "Cotonou",
            "specialty": "Finition",
            "category": "Peinture",
            "description": "Application de peintures décoratives et enduits lisses.",
            "avatar_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=1000&auto=format&fit=crop",
            # Pinceaux et peinture
            "rating": 5.0
        }
    ]

    for u in users_data:
        new_user = models.User(
            username=u["username"],
            email=f"{u['username']}@build.bj",
            hashed_password=get_password_hash("password123"),
            role=u["role"],
            city=u["city"],
            specialty=u.get("specialty"),
            shop_name=u.get("shop_name"),
            category=u["category"],
            description=u["description"],
            avatar_url=u["avatar_url"],
            rating=u["rating"]
        )
        db.add(new_user)

    db.commit()
    print("✅ Seed terminé ! Ton application ressemble maintenant à une vraie plateforme BTP.")


if __name__ == "__main__":
    run_seed()