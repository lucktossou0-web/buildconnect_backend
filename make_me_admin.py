# make_me_admin.py
import os
from sqlalchemy import create_engine, text

# COLLE ICI TON "EXTERNAL DATABASE URL" de Render
DATABASE_URL = "postgresql://chancetossou:hqaCtQSrcSb0wuOopbjfDvMGov02knuN@dpg-d5bcci6r433s738sm0eg-a.virginia-postgres.render.com/buildconnect"

# Correction pour SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def boost_admin(username):
    with engine.connect() as conn:
        # On vérifie si l'utilisateur existe
        result = conn.execute(text(f"SELECT username FROM users WHERE username = '{username}'"))
        user = result.fetchone()

        if user:
            conn.execute(text(f"UPDATE users SET is_admin = true WHERE username = '{username}'"))
            conn.commit()
            print(f"✅ Succès : {username} est maintenant Administrateur sur Render !")
        else:
            print(f"❌ Erreur : L'utilisateur '{username}' n'existe pas sur Render. Inscris-toi d'abord sur le site !")

if __name__ == "__main__":
    pseudo = input("Entre ton pseudo utilisé sur le site en ligne : ")
    boost_admin(pseudo)