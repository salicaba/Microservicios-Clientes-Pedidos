from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

@dataclass
class Pedido:
    id: Optional[int]
    cliente_id: int
    producto: str
    cantidad: int
    total: float
    estado: EstadoPedido
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.id:
            self.fecha_creacion = datetime.now()
            self.estado = EstadoPedido.PENDIENTE
