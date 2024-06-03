import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.Base = Base

    def create_tables(self):
        """
        Cria as tabelas no banco de dados.
        """
        self.Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """
        Retorna uma nova sessão de banco de dados.
        """
        return self.SessionLocal()

    def close(self):
        """
        Fecha a sessão de banco de dados.
        """
        self.SessionLocal.remove()
