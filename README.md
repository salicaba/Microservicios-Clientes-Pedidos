# Microservicios Clientes & Pedidos

## 🚀 Arquitectura Hexagonal con FastAPI, RabbitMQ y Docker

Sistema de microservicios que implementa un CRUD completo para clientes y pedidos, con comunicación HTTP entre servicios y mensajería asíncrona con RabbitMQ.

## 📋 Requisitos

- Docker y Docker Compose
- WSL2 (para Windows) o Linux/Mac

## 🏗️ Estructura del Proyecto
microservicios-clientes-pedidos/
├── clientes-service/ # Microservicio de Clientes
│ ├── domain/ # Capa de dominio (entidades, repositorios)
│ ├── application/ # Capa de aplicación (servicios)
│ └── infrastructure/ # Capa de infraestructura (API, DB, RabbitMQ)
├── pedidos-service/ # Microservicio de Pedidos
│ ├── domain/ # Capa de dominio
│ ├── application/ # Capa de aplicación
│ └── infrastructure/ # Capa de infraestructura
├── docker-compose.yml # Orquestación de servicios
└── README.md # Este archivo

## 🗄️ Bases de Datos

- **Clientes**: MySQL (puerto 33070)
- **Pedidos**: PostgreSQL (puerto 54320)

## 📨 Mensajería

- **RabbitMQ**: Gestión de eventos (puerto 15670)

## 🔌 Endpoints API

### Microservicio de Clientes (http://localhost:8001)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clientes` | Listar todos los clientes |
| POST | `/clientes` | Crear un nuevo cliente |
| GET | `/clientes/{id}` | Obtener cliente por ID |
| PUT | `/clientes/{id}` | Actualizar cliente completo |
| DELETE | `/clientes/{id}` | Eliminar cliente |

### Microservicio de Pedidos (http://localhost:8002)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/pedidos` | Listar todos los pedidos |
| POST | `/pedidos` | Crear un nuevo pedido |
| GET | `/pedidos/{id}` | Obtener pedido por ID |
| PUT | `/pedidos/{id}` | Actualizar pedido completo |
| DELETE | `/pedidos/{id}` | Eliminar pedido |
| GET | `/clientes/{id}/pedidos` | Listar pedidos de un cliente |

## 🚀 Cómo Ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/microservicios-clientes-pedidos.git
cd microservicios-clientes-pedidos

# Levantar todos los servicios
docker-compose up -d

# Verificar que todos los contenedores están funcionando
docker-compose ps

# Ver logs
docker-compose logs -f
📚 Documentación Interactiva
Clientes API: http://localhost:8001/docs

Pedidos API: http://localhost:8002/docs

RabbitMQ Management: http://localhost:15670 (admin/admin123)

🔗 Comunicación entre Servicios
HTTP: Pedidos valida la existencia de clientes mediante llamadas HTTP al servicio de clientes

RabbitMQ: Eventos de clientes (creación, actualización, eliminación) se publican y son consumidos por pedidos
🧪 Probar CRUD Completo
bash
# Crear un cliente
curl -X POST http://localhost:8001/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "email": "juan@email.com", "telefono": "555-1234"}'

# Crear un pedido para ese cliente
curl -X POST http://localhost:8002/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": 1, "producto": "Laptop", "cantidad": 1, "total": 999.99}'

# Listar todos los pedidos
curl http://localhost:8002/pedidos

# Actualizar un pedido
curl -X PUT http://localhost:8002/pedidos/1 \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": 1, "producto": "Laptop Pro", "cantidad": 2, "total": 1999.98}'

# Eliminar un pedido
curl -X DELETE http://localhost:8002/pedidos/1
🛠️ Tecnologías Utilizadas
FastAPI - Framework web para las APIs

SQLAlchemy - ORM para bases de datos

MySQL - Base de datos para clientes

PostgreSQL - Base de datos para pedidos

RabbitMQ - Mensajería asíncrona

Docker - Contenedorización

Python 3.11 - Lenguaje de programación

📊 Arquitectura
text
                    ┌─────────────────┐
                    │   Cliente API   │
                    │   (Port 8001)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     MySQL       │
                    │   (Port 33070)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    RabbitMQ     │
                    │  (Port 15670)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Pedido API    │
                    │   (Port 8002)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL    │
                    │   (Port 54320)  │
                    └─────────────────┘

