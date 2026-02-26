#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional #importacion para los parametros opcionales
from pydantic import BaseModel #importacion para la validacion de datos, se crea una clase que hereda de BaseModel y se definen los campos que se esperan recibir en el endpoint, con su tipo de dato correspondiente
from pydantic import Field #importacion para agregar validaciones adicionales a los campos del modelo, como longitud mínima, máxima, expresiones regulares, etc.

#intancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="Emiliano Ledesma",
    version="1.0"
)

#tabla ficticia
usuarios=[
    {"id":1, "Nombre":"Diego", "Edad":21},
    {"id":2, "Nombre":"Coral", "Edad":20},
    {"id":3, "Nombre":"Saul", "Edad":24},
]

#Modelo pydantic para la validacion de datos
class Crear_Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example = "Emiliano Ledesma")
    Edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 - 125")

#endpoints
@app.get("/",tags=['Inicio'])
async def bienvenida():
    return {"mensaje":"Bienvenido a FastAPI"} #Primero la clave (como si fuera el index) y luego el valor de la clave (en este caso el mensaje a entregar)

@app.get("/holaMundo", tags=['Asincronia'])
async def hola():
    await asyncio.sleep(5) #peticion, consulta BD, Archivo 
    return {
        "mensaje":"Hola Mundo!",
        "Status":"200"
    }
    
@app.get("/v1/ParametroOB/{id}",tags=['Parametro Obligatorio']) #con las llaves especificas que se necesita un parametro, en este caso una id
async def consultaUno(id:int): #forza una validacion de que el parametro id sea un entero
    return {"mensaje":"Usuario Encontrado",
            "Usuario":id,
            "status":200}

@app.get("/v1/ParametrosOp/",tags=['Parametro Opcional']) #No puede haber enpoints del mismo metodo con el mismo nombre, se eliminan las llaves que especifican el parametro
async def consultaTodos(id:Optional[int]=None): #La funcion tampoco se puede llamar igual. El parametro ahora cambia a opcional con [int] y con =None se manda a nulo en caso de que no haya valor.
    if id is not None: #cuando encuentra el usuario
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {
                    "Mensaje":"Usuario Encontrado",
                    "Usuario": usuariok,
                    "status":"200"
                }
        return { #cuando no encuentra al usuario
            "Mensaje":"Usuario No encontrado",
            "status":"404"
        }
    else:
        return { #cuando no se proporciona usuario
            "Mensaje":"No se proporciono id",
            "status": "204"
        }

@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def consultaT():
    return {
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

@app.post("/v1/usuarios/",tags=['CRUD HTTP'])
async def agregar_usuario(usuario:Crear_Usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code= 400,
                detail= "El id ya existe"
                )
    usuarios.append(usuario)
    return {
        "status":"200",
        "Mensaje":"Usuario agregado",
        "usuario":usuario
    }
    

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario["id"]:
            usr["Nombre"] = usuario["Nombre"]
            usr["Edad"]   = usuario["Edad"]

            return {
                "status":"200",
                "Mensaje": "Usuario actualizado",
                "usuario": usr
            }
    raise HTTPException(
        status_code=404,
        detail=f"El usuario con id {usuario['id']} no existe"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "status":"200",
                "Mensaje": "Usuario eliminado",
                "usuario": eliminado
            }
    raise HTTPException(
        status_code=404,
        detail=f"El usuario con id {id} no existe"
    )
