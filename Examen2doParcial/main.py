from fastapi import FastAPI,HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Literal 
from datetime import datetime, time
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets #para contraseñas, hashes y ese pedo

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

#Seguridad de endpoints con HTTPBasic

Security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(Security)):
    usuario_auth = secrets.compare_digest(credenciales.username,"banco")
    contra_auth = secrets.compare_digest(credenciales.password, "2468")
    
    if not(usuario_auth and contra_auth):
        raise HTTPException(
                status_code= 401,
                detail= "Credenciales no autorizadas"
                )
    
    return credenciales.username


class Crear_Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    Nombre: str = Field(..., min_length=8, max_length=50, description="Nombre del usuario", example = "Emiliano Ledesma")
    
class Crear_Turno(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de turno")
    TipoTramite: Literal["Deposito", "Retiro", "Consulta"] = Field(..., description="Tipo de Tramite", example = "Deposito")
    fecha_turno: datetime = Field(..., description="Fecha y hora de la reserva (futura, 9 am y 3 PM)", example="2026-03-15T19:00:00")
    Estado: Literal["Disponible", "Ocupado"] = Field(..., description="Estado del Turno", example = "Disponible")


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

@app.post("/v1/Turnos/", tags=["Reservas"], status_code=status.HTTP_201_CREATED)
async def crear_Turnos(turno: Crear_Turno):
    if turno.fecha_turno <= datetime.now():
        raise HTTPException(status_code=400, detail="La fecha de turno debe ser futura")      
    if not (time(9, 0) <= turno.fecha_turno.time() <= time(15, 0)):
        raise HTTPException(status_code=400, detail="Horario valido: 8:00am - 10:00pm")        

    nuevo_id = max(t["id"] for t in turno) + 1 if turno else 1
    nuevo_turno = {
        "id": nuevo_id,
        "fecha_turno": Turnos.fecha_reserva.isoformat(),
        "estado":"No disponible"
    }
    Turnos.append(nuevo_turno)
    return {
        "status": "201", 
        "mensaje": "Reserva creada exitosamente",
        "reserva": nuevo_turno
    }

@app.get("/v1/Turnos/disponibles", tags=['Turnos'])
async def Turnos_disponibles():
    disponibles = [Tu for Tu in Turnos if Tu["Estado"] == "Disponible"]
    return {
        "status": "200",
        "total": len(disponibles),
        "Turnos": disponibles
    }

@app.get("/v1/Turnos/{id}",tags=['Turnos']) #con las llaves especificas que se necesita un parametro, en este caso una id
async def consultaID(id:int): #forza una validacion de que el parametro id sea un entero
    return {"mensaje":"Usuario Encontrado",
            "Usuario":id,
            "status":200}

@app.put("/v1/Turnos/{Turno_id}/actualizar", tags=['Turnos'], status_code=status.HTTP_200_OK)
async def Atender_turno(Turno_id: int,  usuario_auth: str = Depends(verificar_peticion)):
    Turno = next((Tu for Tu in Turnos if Tu["id"] == Turno_id), None)
    if not Turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    if Turnos["Estado"] == "Disponible":
        raise HTTPException(status_code=409, detail="El Turno esta disponible")
    
    Turnos["Estado"] = "Atendido"
    return {
        "status": "200",
        "Mensaje": "Turno Marcado como Atendido",
        "Turno": Turno
    }
    
@app.delete("/v1/Turnos/{turno_id}", tags=['Turnos'], status_code=status.HTTP_200_OK, )
async def eliminar_turno(turno_id: int,  usuario_auth: str = Depends(verificar_peticion)):
    turno = next((t for t in Turnos if t["id"] == turno_id), None)
    if not turno:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo no existe")
    Turnos.remove(turno)
    return {
        "status": "200",
        "Turno Eliminado": turno
    }