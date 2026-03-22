from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from infrastructure.db.database import get_db, init_db
from infrastructure.repositories.mysql_cliente_repository import MySQLClienteRepository
from infrastructure.message_bus.rabbitmq_producer import RabbitMQProducer
from application.services.cliente_service import ClienteService

app = FastAPI(title="Microservicio de Clientes", version="1.0.0")

# Modelos Pydantic para la API
class ClienteCreate(BaseModel):
    nombre: str
    email: str
    telefono: str

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    fecha_registro: datetime
    
    class Config:
        from_attributes = True

# Dependencias
def get_cliente_service(db: Session = Depends(get_db)):
    repository = MySQLClienteRepository(db)
    return ClienteService(repository)

def get_rabbitmq_producer():
    producer = RabbitMQProducer()
    try:
        yield producer
    finally:
        producer.close()

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Base de datos inicializada")

# ==================== GETS ====================
@app.get("/clientes", response_model=List[ClienteResponse])
async def listar_clientes(service: ClienteService = Depends(get_cliente_service)):
    """Listar todos los clientes"""
    clientes = await service.listar_clientes()
    return clientes

@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(cliente_id: int, service: ClienteService = Depends(get_cliente_service)):
    """Obtener un cliente por ID"""
    cliente = await service.obtener_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# ==================== POST ====================
@app.post("/clientes", response_model=ClienteResponse)
async def crear_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service),
    producer: RabbitMQProducer = Depends(get_rabbitmq_producer)
):
    """Crear un nuevo cliente"""
    nuevo_cliente = await service.crear_cliente(
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono
    )
    
    producer.publish_event(
        'CLIENTE_CREADO',
        {
            'id': nuevo_cliente.id,
            'nombre': nuevo_cliente.nombre,
            'email': nuevo_cliente.email
        }
    )
    
    return nuevo_cliente

# ==================== PUT ====================
@app.put("/clientes/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service),
    producer: RabbitMQProducer = Depends(get_rabbitmq_producer)
):
    """Actualizar un cliente completo"""
    cliente_actualizado = await service.actualizar_cliente(
        id=cliente_id,
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono
    )
    
    if not cliente_actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    producer.publish_event(
        'CLIENTE_ACTUALIZADO',
        {'id': cliente_id, 'email': cliente.email}
    )
    
    return cliente_actualizado

# ==================== DELETE ====================
@app.delete("/clientes/{cliente_id}")
async def eliminar_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
    producer: RabbitMQProducer = Depends(get_rabbitmq_producer)
):
    """Eliminar un cliente"""
    eliminado = await service.eliminar_cliente(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    producer.publish_event(
        'CLIENTE_ELIMINADO',
        {'id': cliente_id}
    )
    
    return {"message": "Cliente eliminado correctamente"}