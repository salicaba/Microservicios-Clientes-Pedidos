from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from domain.models.pedido import Pedido, EstadoPedido
from domain.repositories.pedido_repository import PedidoRepository
from infrastructure.db.database import PedidoDB, EstadoPedidoDB

class PostgresPedidoRepository(PedidoRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, pedido: Pedido) -> Pedido:
        db_pedido = PedidoDB(
            cliente_id=pedido.cliente_id,
            producto=pedido.producto,
            cantidad=pedido.cantidad,
            total=pedido.total,
            estado=EstadoPedidoDB(pedido.estado.value),
            fecha_creacion=datetime.now()
        )
        self.db.add(db_pedido)
        self.db.commit()
        self.db.refresh(db_pedido)
        
        return Pedido(
            id=db_pedido.id,
            cliente_id=db_pedido.cliente_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=EstadoPedido(db_pedido.estado.value),
            fecha_creacion=db_pedido.fecha_creacion,
            fecha_actualizacion=db_pedido.fecha_actualizacion
        )
    
    async def get_by_id(self, id: int) -> Optional[Pedido]:
        db_pedido = self.db.query(PedidoDB).filter(PedidoDB.id == id).first()
        if not db_pedido:
            return None
        
        return Pedido(
            id=db_pedido.id,
            cliente_id=db_pedido.cliente_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=EstadoPedido(db_pedido.estado.value),
            fecha_creacion=db_pedido.fecha_creacion,
            fecha_actualizacion=db_pedido.fecha_actualizacion
        )
    
    async def get_by_cliente(self, cliente_id: int) -> List[Pedido]:
        db_pedidos = self.db.query(PedidoDB).filter(PedidoDB.cliente_id == cliente_id).all()
        return [
            Pedido(
                id=p.id,
                cliente_id=p.cliente_id,
                producto=p.producto,
                cantidad=p.cantidad,
                total=p.total,
                estado=EstadoPedido(p.estado.value),
                fecha_creacion=p.fecha_creacion,
                fecha_actualizacion=p.fecha_actualizacion
            ) for p in db_pedidos
        ]
    
    async def update_estado(self, id: int, estado: EstadoPedido) -> Optional[Pedido]:
        db_pedido = self.db.query(PedidoDB).filter(PedidoDB.id == id).first()
        if not db_pedido:
            return None
        
        db_pedido.estado = EstadoPedidoDB(estado.value)
        db_pedido.fecha_actualizacion = datetime.now()
        
        self.db.commit()
        self.db.refresh(db_pedido)
        
        return Pedido(
            id=db_pedido.id,
            cliente_id=db_pedido.cliente_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=EstadoPedido(db_pedido.estado.value),
            fecha_creacion=db_pedido.fecha_creacion,
            fecha_actualizacion=db_pedido.fecha_actualizacion
        )
    
    async def update_complete(self, id: int, pedido: Pedido) -> Optional[Pedido]:
        """Actualizar completamente un pedido"""
        db_pedido = self.db.query(PedidoDB).filter(PedidoDB.id == id).first()
        if not db_pedido:
            return None
        
        db_pedido.cliente_id = pedido.cliente_id
        db_pedido.producto = pedido.producto
        db_pedido.cantidad = pedido.cantidad
        db_pedido.total = pedido.total
        db_pedido.estado = EstadoPedidoDB(pedido.estado.value)
        db_pedido.fecha_actualizacion = datetime.now()
        
        self.db.commit()
        self.db.refresh(db_pedido)
        
        return Pedido(
            id=db_pedido.id,
            cliente_id=db_pedido.cliente_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=EstadoPedido(db_pedido.estado.value),
            fecha_creacion=db_pedido.fecha_creacion,
            fecha_actualizacion=db_pedido.fecha_actualizacion
        )
    
    async def delete(self, id: int) -> bool:
        """Eliminar un pedido"""
        db_pedido = self.db.query(PedidoDB).filter(PedidoDB.id == id).first()
        if not db_pedido:
            return False
        
        self.db.delete(db_pedido)
        self.db.commit()
        return True
    
    async def get_all(self) -> List[Pedido]:
        """Listar todos los pedidos"""
        db_pedidos = self.db.query(PedidoDB).all()
        return [
            Pedido(
                id=p.id,
                cliente_id=p.cliente_id,
                producto=p.producto,
                cantidad=p.cantidad,
                total=p.total,
                estado=EstadoPedido(p.estado.value),
                fecha_creacion=p.fecha_creacion,
                fecha_actualizacion=p.fecha_actualizacion
            ) for p in db_pedidos
        ]