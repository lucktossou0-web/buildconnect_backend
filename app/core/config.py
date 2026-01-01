import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "BuildConnect"
    PROJECT_VERSION: str = "1.0.0"

    # 1. On tente d'abord de récupérer l'URL complète (donnée par Render)
    DATABASE_URL = os.getenv("DATABASE_URL")

    # 2. Si DATABASE_URL n'existe pas, on la construit (cas du local)
    if not DATABASE_URL:
        POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
        POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB = os.getenv("POSTGRES_DB", "buildconnect")
        DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # 3. FIX CRUCIAL POUR RENDER :
    # SQLAlchemy exige "postgresql://" mais Render donne souvent "postgres://"
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "UNE_CLE_TRES_SECRETE_12345")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 heures


settings = Settings()