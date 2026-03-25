#importaciones
from fastapi import FastAPI, APIRouter
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine) 

#intancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="Emiliano Ledesma",
    version="1.0"
)

#Router de Endpoints disponibles
app.include_router(usuarios.router)
app.include_router(varios.routerV)


