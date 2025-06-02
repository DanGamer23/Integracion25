
# INTEGRACION25 - Sistema de Gestión para FERREMAS 

Este proyecto integra múltiples tecnologías para ofrecer una plataforma completa de comercio electrónico y gestión interna para la empresa ficticia **FERREMAS**, dedicada a la venta de herramientas y productos industriales.

##  Tecnologías utilizadas

- **Django** (frontend web + cliente)
- **FastAPI** (gestión de usuarios, login, registro)
- **Spring Boot** (API de productos, pedidos y pagos)
- **Oracle Database** (modelo relacional centralizado)
- **Docker + Docker Compose** (entorno de ejecución completo)
- **API externa**: valor del dólar (para conversión de precios) y Mercado Pago

##  Funcionalidades principales

### Cliente
- Registro e inicio de sesión
- Catálogo de productos
- Carrito de compras
- Pago con tarjeta (simulado) o transferencia
- Seguimiento de pedidos en "Mis Compras"
- Visualización de precio en pesos y dólares (USD)

### Panel de Administración (según rol)
- **Contador**: aprobación de pagos por transferencia
- **Bodeguero**: preparación de pedidos y marcar como "listo"
- **Vendedor**: entrega de productos y cierre de pedidos
- **Administrador**: CRUD de productos, usuarios y control general
- **Dashboard** con métricas del sistema

##  Estructura del proyecto

```
INTEGRACION25/
├── web/           ← Django (clientes, panel, carrito)
├── API1/          ← FastAPI (usuarios, login y pagos)
├── API2/          ← Spring Boot (productos)
├── BD/            ← Scripts SQL para Oracle y datos extra
├── docker-compose.yml
├── README.md
└── ...
```

##  Cómo ejecutar el proyecto (con Docker)

```bash
docker compose up --build
```
##  Ejecutar Scripts
Conectarse a la base de datos como system
Username: SYSTEM   
Pass: 123456
hostname: localhost
Port: 1522
Service Name: XEPDB1
Ejecutar script 1 como SYSTEM
Conectarse a la BD como FERREMAS
y ejecutar script 2


El sistema levantará automáticamente:

- Base de datos Oracle
- API1 (FastAPI)
- API2 (Spring Boot)
- Frontend Django

## 🧪 Pruebas básicas

1. Acceder a `http://127.0.0.1:8001`
2. Registrarse como cliente
3. Agregar productos al carrito
5. Iniciar sesión como administrador (`rol_id = 5`) para acceder al panel


