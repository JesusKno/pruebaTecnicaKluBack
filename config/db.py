from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del .env

DATABASE_URL = os.getenv("DB_URL")  # Cambia a PostgreSQL si es necesario

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas si no existen
from models.transacciones import Base
Base.metadata.create_all(bind=engine)