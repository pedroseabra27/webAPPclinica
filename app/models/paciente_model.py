from sqlalchemy import Column, Integer, String, Text
from app.database import Base, engine # Importar engine para criar a tabela

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    idade = Column(Integer, nullable=False)
    endereco = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    queixa_principal = Column(Text, nullable=True)

# Criar a tabela no banco de dados se ela não existir
# Isso deve ser chamado uma vez, idealmente no início da aplicação.
# Podemos colocar em app_web.py ou chamar init_db() de database.py
Base.metadata.create_all(bind=engine)
