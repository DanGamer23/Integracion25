from fastapi import FastAPI
from routers import clientes # Importamos el router de clientes
from routers import pagos  # Importamos el router de pagos
from routers import pedidos  # Importamos el router de pedidos

app = FastAPI(
    title="API de gestion de clientes",
    version="1.1.0",
    description="API para la gestion de clientes de la empresa FERREMAS"
)

app.include_router(clientes.router)
app.include_router(pagos.router)
app.include_router(pedidos.router)
