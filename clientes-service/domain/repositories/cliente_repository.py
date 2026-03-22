from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.cliente import Cliente

class ClienteRepository(ABC):
    @abstractmethod
    async def create(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Cliente]:
        pass
    
    @abstractmethod
    async def update(self, id: int, cliente: Cliente) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass