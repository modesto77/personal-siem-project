from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Création d'un fichier local SQLite nommé 'siem.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./siem.db"

# L'argument check_same_thread est nécessaire pour SQLite avec FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Configuration de la session de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour nos modèles de tables
Base = declarative_base()

# Fonction utilitaire pour ouvrir/fermer une session DB par requête API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()