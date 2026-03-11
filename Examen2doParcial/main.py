from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal 
from datetime import datetime

app = FastAPI (
    title = 'Turnos Bancarios',
    Description = 'Sistema de Turnos Bancarios',
)

usuarios = [
    {"id":1, "Nombre":"Emiliano"}
]

Turnos = [
    {"id":1, "Tipo_Tramite":"Deposito", "Fecha":"11-3-2026T14:20:00", "Estado":"Disponible"}
]

class Crear_Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    Nombre: str = Field(..., min_length=8, max_length=50, description="Nombre del usuario", example = "Emiliano Ledesma")
    
class Crear_Turno(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de turno")
    TipoTramite: Literal["Deposito", "Retiro", "Consulta"] = Field(..., description="Tipo de Tramite", example = "Deposito")
    fecha_turno: datetime = Field(..., description="Fecha y hora de la reserva (futura, 9 am y 3 PM)", example="2026-03-15T19:00:00")
    Estado: Literal["Disponible", "Ocupado"] = Field(..., description="Estado del Turno", example = "Disponible")


@app.get("/v1/Turnos/disponibles", tags=['Turnos'])
async def Turnos_disponibles():
    disponibles = [Tu for Tu in Turnos if Tu["Estado"] == "Disponible"]
    return {
        "status": "200",
        "total": len(disponibles),
        "Turnos": disponibles
    }
    
@app.post("/v1/Turnos/", tags=['Turnos'], status_code=status.HTTP_201_CREATED)
async def agregar_Turno(Turno: Crear_Turno):
    for Tu in Turnos:
        if Tu["id"] == Turno.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El id ya existe")
        return {
        "status":"201",
        "Mensaje":"Libro agregado",
        "Turno":Turno
    }
        
@app.get("/v1/Turnos/{id}",tags=['Turnos']) #con las llaves especificas que se necesita un parametro, en este caso una id
async def consultaID(id:int): #forza una validacion de que el parametro id sea un entero
    return {"mensaje":"Usuario Encontrado",
            "Usuario":id,
            "status":200}
    