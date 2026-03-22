from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import threading

from infrastructure.db.database import get_db, init_db
from infrastructure.repositories.postgres_pedido_repository import PostgresPedidoRepository
from application.services.pedido_service import PedidoService
from application.consumers.cliente_event_consumer import ClienteEventConsumer
from domain.models.pedido import EstadoPedido

app = FastAPI(title="Microservicio de Pedidos", version="1.0.0")

# Modelos Pydantic para la API
class PedidoCreate(BaseModel):
    cliente_id: int
    producto: str
    cantidad: int
    total: float
    estado: str = "pendiente"

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    producto: str
    cantidad: int
    total: float
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime = None
    
    class Config:
        from_attributes = True

# Dependencias
def get_pedido_service(db: Session = Depends(get_db)):
    repository = PostgresPedidoRepository(db)
    return PedidoService(repository)

# Event consumer callback
def handle_cliente_event(event):
    print(f"Evento de cliente recibido: {event}")

consumer = None

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Base de datos inicializada")
    
    global consumer
    consumer = ClienteEventConsumer(handle_cliente_event)
    consumer.start()
    print("Consumer de eventos iniciado")

@app.on_event("shutdown")
async def shutdown_event():
    if consumer:
        consumer.stop()
        print("Consumer detenido")

# ==================== GETS ====================
@app.get("/pedidos", response_model=List[PedidoResponse])
async def listar_pedidos(service: PedidoService = Depends(get_pedido_service)):
    """Listar todos los pedidos"""
    pedidos = await service.listar_todos_pedidos()
    return pedidos

@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    """Obtener un pedido por ID"""
    pedido = await service.obtener_pedido(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.get("/clientes/{cliente_id}/pedidos", response_model=List[PedidoResponse])
async def listar_pedidos_por_cliente(cliente_id: int, service: PedidoService = Depends(get_pedido_service)):
    """Listar todos los pedidos de un cliente específico"""
    pedidos = await service.listar_pedidos_cliente(cliente_id)
    return pedidos

# ==================== POST ====================
@app.post("/pedidos", response_model=PedidoResponse)
async def crear_pedido(
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service)
):
    """Crear un nuevo pedido"""
    nuevo_pedido = await service.crear_pedido(
        cliente_id=pedido.cliente_id,
        producto=pedido.producto,
        cantidad=pedido.cantidad,
        total=pedido.total,
        estado=pedido.estado
    )
    
    if not nuevo_pedido:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return nuevo_pedido

# ==================== PUT ====================
@app.put("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def actualizar_pedido(
    pedido_id: int,
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service)
):
    """Actualizar un pedido completo"""
    pedido_existente = await service.obtener_pedido(pedido_id)
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    if not await service._validar_cliente(pedido.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    pedido_actualizado = await service.actualizar_pedido_completo(
        pedido_id=pedido_id,
        cliente_id=pedido.cliente_id,
        producto=pedido.producto,
        cantidad=pedido.cantidad,
        total=pedido.total,
        estado=pedido.estado
    )
    
    if not pedido_actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return pedido_actualizado

# ==================== DELETE ====================
@app.delete("/pedidos/{pedido_id}", response_model=dict)
async def eliminar_pedido(
    pedido_id: int,
    service: PedidoService = Depends(get_pedido_service)
):
    """Eliminar un pedido"""
    eliminado = await service.eliminar_pedido(pedido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return {"message": "Pedido eliminado correctamente", "id": pedido_id}