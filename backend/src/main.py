from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_db_and_tables
from routers.database_router import router as database_router
from routers.usuario_router import router as usuario_router
from routers.reserva_router import router as reserva_router

# Registrar modelos antes de create_all()
from models.usuario_model import Usuario
from models.reserva_model import Reserva


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()

    yield


app = FastAPI(
    title="API de Usuarios y Reservas",
    description=(
        "API REST desarrollada con FastAPI, "
        "SQLModel y Amazon RDS PostgreSQL"
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(usuario_router)
app.include_router(reserva_router)
app.include_router(database_router)

@app.get(
    "/",
    tags=["Inicio"]
)
def root():

    return {
        "mensaje": "API funcionando correctamente",
        "documentacion": "/docs"
    }
