import asyncio
from typing import Optional #importacion para los parametros opcionales
from app.data.database import usuarios
from fastapi import APIRouter

routerV = APIRouter(tags=['Inicio'])
#endpoints
@routerV.get("/")
async def bienvenida():
    return {"mensaje":"Bienvenido a FastAPI"} #Primero la clave (como si fuera el index) y luego el valor de la clave (en este caso el mensaje a entregar)

@routerV.get("/holaMundo")
async def hola():
    await asyncio.sleep(5) #peticion, consulta BD, Archivo 
    return {
        "mensaje":"Hola Mundo!",
        "Status":"200"
    }
    
@routerV.get("/v1/ParametroOB/{id}") #con las llaves especificas que se necesita un parametro, en este caso una id
async def consultaUno(id:int): #forza una validacion de que el parametro id sea un entero
    return {"mensaje":"Usuario Encontrado",
            "Usuario":id,
            "status":200}

@routerV.get("/v1/ParametrosOp/") #No puede haber enpoints del mismo metodo con el mismo nombre, se eliminan las llaves que especifican el parametro
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