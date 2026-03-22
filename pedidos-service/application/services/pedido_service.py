from typing import List, Optional
import httpx
import os
from domain.models.pedido import Pedido, EstadoPedido
from domain.repositories.pedido_repository import PedidoRepository

class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository
        self.clientes_service_url = os.getenv("CLIENTES_SERVICE_URL", "http://localhost:8001")
    
    async def _validar_cliente(self, cliente_id: int) -> bool:
        """Valida que el cliente exista llamando al microservicio de clientes"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.clientes_service_url}/clientes/{cliente_id}")
                return response.status_code == 200
        except Exception as e:
            print(f"Error validando cliente: {e}")
            return False
    
    async def crear_pedido(self, cliente_id: int, producto: str, cantidad: int, total: float) -> Optional[Pedido]:
        # Validar que el cliente existe
        if not await self._validar_cliente(cliente_id):
            return None
        
        pedido = Pedido(
            id=None,
            cliente_id=cliente_id,
            producto=producto,
            cantidad=cantidad,
            total=total,
            estado=EstadoPedido.PENDIENTE,
            fecha_creacion=None,
            fecha_actualizacion=None
        )
        
        return await self.repository.create(pedido)
    
    async def obtener_pedido(self, id: int) -> Optional[Pedido]:
        return await self.repository.get_by_id(id)
    
    async def listar_pedidos_cliente(self, cliente_id: int) -> List[Pedido]:
        return await self.repository.get_by_cliente(cliente_id)
    
    async def actualizar_estado(self, id: int, estado: EstadoPedido) -> Optional[Pedido]:
        return await self.repository.update_estado(id, estado)

    # Agregar después del método actualizar_estado

async def actualizar_pedido_completo(
    self, 
    pedido_id: int, 
    cliente_id: int, 
    producto: str, 
    cantidad: int, 
    total: float,
    estado: str = "pendiente"
) -> Optional[Pedido]:
    """Actualizar completamente un pedido"""
    # Validar que el cliente existe
    if not await self._validar_cliente(cliente_id):
        return None
    
    try:
        estado_enum = EstadoPedido(estado)
    except ValueError:
        estado_enum = EstadoPedido.PENDIENTE
    
    pedido = Pedido(
        id=pedido_id,
        cliente_id=cliente_id,
        producto=producto,
        cantidad=cantidad,
        total=total,
        estado=estado_enum,
        fecha_creacion=None,
        fecha_actualizacion=datetime.now()
    )
    
    return await self.repository.update_complete(pedido_id, pedido)

async def listar_todos_pedidos(self) -> List[Pedido]:
    """Listar todos los pedidos"""
    return await self.repository.get_all()