from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user_pedidos:pedidos123@localhost:5432/pedidos_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EstadoPedidoDB(enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class PedidoDB(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False, index=True)
    producto = Column(String(200), nullable=False)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(Enum(EstadoPedidoDB), default=EstadoPedidoDB.PENDIENTE)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_actualizacion = Column(DateTime, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
