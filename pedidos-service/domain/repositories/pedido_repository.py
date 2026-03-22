from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.pedido import Pedido

class PedidoRepository(ABC):
    @abstractmethod
    async def create(self, pedido: Pedido) -> Pedido:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    async def get_by_cliente(self, cliente_id: int) -> List[Pedido]:
        pass
    
    @abstractmethod
    async def update_estado(self, id: int, estado: str) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    async def update_complete(self, id: int, pedido: Pedido) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass