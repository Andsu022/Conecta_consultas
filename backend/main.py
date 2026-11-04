# Criação de rotas e API REST no FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.db import init_db

from fastapi import FastAPI
from backend.routes.route_consulta import router as consulta_router
from backend.routes.route_medico import router as medico_router
from backend.routes.route_paciente import router as paciente_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)


app.include_router(medico_router)
app.include_router(paciente_router)
app.include_router(consulta_router)