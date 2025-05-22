from fastapi import FastAPI
from routers import clientes

app = FastAPI(
    title="API de gestion de clientes",
    version="1.1.0",
    description="API para la gestion de clientes de la empresa FERREMAS"
)

app.include_router(clientes.router)