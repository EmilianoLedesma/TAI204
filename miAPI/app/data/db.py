from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

#1. Definimos la URL de la conexion
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )

#2. Creamos el motor de la conexion
engine = create_engine(DATABASE_URL)

#3. Creamos la gestion de sessiones
sessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

#4. Base declarativa para Modelos
Base = declarative_base()

#5. Funcion que trabaja las sesiones con las peticiones
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()