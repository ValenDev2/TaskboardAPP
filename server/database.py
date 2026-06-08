# database.py — Configura la conexión con la base de datos
#
# SQLAlchemy es un ORM (Object Relational Mapper):
# te deja trabajar con la DB usando clases Python en vez de SQL crudo.
# Ejemplo: en vez de  SELECT * FROM users  escribís  db.query(User).all()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from server.config import settings

# Engine = la conexión real con el archivo .db
# check_same_thread=False es necesario solo para SQLite con FastAPI
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal es la "fábrica" que crea sesiones de DB
# Cada request del cliente abre una sesión y la cierra al terminar
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase padre de todos los modelos (tablas)
# Cuando un modelo hereda de Base, SQLAlchemy sabe que es una tabla
class Base(DeclarativeBase):
    pass

# get_db es un generador que FastAPI usa como dependencia
# Cada endpoint que lo necesite recibe una sesión limpia y la cierra solo
def get_db():
    db = SessionLocal()
    try:
        yield db        # yield = "acá está tu sesión, usala"
    finally:
        db.close()      # siempre se cierra, incluso si hay error