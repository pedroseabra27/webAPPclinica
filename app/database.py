from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./clinicadata.db"  # Arquivo do banco de dados SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # check_same_thread é necessário para SQLite com Dash/Flask

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Importar todos os modelos aqui para que sejam registrados corretamente no metadata
    # Ex: from .models import paciente_model
    # Base.metadata.create_all(bind=engine)
    # Por enquanto, vamos chamar create_all diretamente após a definição do modelo
    pass
