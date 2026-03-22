from typing import List, Optional
from domain.models.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository
    
    async def crear_cliente(self, nombre: str, email: str, telefono: str) -> Cliente:
        cliente = Cliente(
            id=None,
            nombre=nombre,
            email=email,
            telefono=telefono,
            fecha_registro=None
        )
        return await self.repository.create(cliente)
    
    async def obtener_cliente(self, id: int) -> Optional[Cliente]:
        return await self.repository.get_by_id(id)
    
    async def listar_clientes(self) -> List[Cliente]:
        return await self.repository.get_all()
    
    async def actualizar_cliente(self, id: int, nombre: str, email: str, telefono: str) -> Optional[Cliente]:
        cliente = Cliente(
            id=id,
            nombre=nombre,
            email=email,
            telefono=telefono,
            fecha_registro=None
        )
        return await self.repository.update(id, cliente)
    
    async def eliminar_cliente(self, id: int) -> bool:
        return await self.repository.delete(id)
