# buildconnect_backend/setup_db.py

import sys
import os

# Ajoute le dossier courant au chemin de recherche Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from app.db.base import Base  # On importe Base depuis db.base pour inclure les modèles

def init_db():
    print("Connexion à PostgreSQL en cours...")
    try:
        print("✅ Succès : Les tables ont été créées dans la base de données.")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        print("\nConseils :")
        print("1. Vérifie que PostgreSQL est lancé.")
        print("2. Vérifie que la base de données existe (CREATE DATABASE buildconnect;).")
        print("3. Vérifie tes identifiants dans le fichier .env.")

if __name__ == "__main__":
    init_db()