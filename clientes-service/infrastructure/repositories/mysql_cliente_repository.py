from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository
from infrastructure.db.database import ClienteDB
from datetime import datetime

class MySQLClienteRepository(ClienteRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, cliente: Cliente) -> Cliente:
        db_cliente = ClienteDB(
            nombre=cliente.nombre,
            email=cliente.email,
            telefono=cliente.telefono,
            fecha_registro=datetime.now()
        )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        
        return Cliente(
            id=db_cliente.id,
            nombre=db_cliente.nombre,
            email=db_cliente.email,
            telefono=db_cliente.telefono,
            fecha_registro=db_cliente.fecha_registro
        )
    
    async def get_by_id(self, id: int) -> Optional[Cliente]:
        db_cliente = self.db.query(ClienteDB).filter(ClienteDB.id == id).first()
        if not db_cliente:
            return None
        
        return Cliente(
            id=db_cliente.id,
            nombre=db_cliente.nombre,
            email=db_cliente.email,
            telefono=db_cliente.telefono,
            fecha_registro=db_cliente.fecha_registro
        )
    
    async def get_all(self) -> List[Cliente]:
        db_clientes = self.db.query(ClienteDB).all()
        return [
            Cliente(
                id=c.id,
                nombre=c.nombre,
                email=c.email,
                telefono=c.telefono,
                fecha_registro=c.fecha_registro
            ) for c in db_clientes
        ]
    
    async def update(self, id: int, cliente: Cliente) -> Optional[Cliente]:
        db_cliente = self.db.query(ClienteDB).filter(ClienteDB.id == id).first()
        if not db_cliente:
            return None
        
        db_cliente.nombre = cliente.nombre
        db_cliente.email = cliente.email
        db_cliente.telefono = cliente.telefono
        
        self.db.commit()
        self.db.refresh(db_cliente)
        
        return Cliente(
            id=db_cliente.id,
            nombre=db_cliente.nombre,
            email=db_cliente.email,
            telefono=db_cliente.telefono,
            fecha_registro=db_cliente.fecha_registro
        )
    
    async def delete(self, id: int) -> bool:
        db_cliente = self.db.query(ClienteDB).filter(ClienteDB.id == id).first()
        if not db_cliente:
            return False
        
        self.db.delete(db_cliente)
        self.db.commit()
        return True
