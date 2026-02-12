#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional #importacion para los parametros opcionales
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
    
@app.get("/v1/usuario{id}",tags=['Parametro Obligatorio']) #con las llaves especificas que se necesita un parametro, en este caso una id
async def consultaUno(id:int): #forza una validacion de que el parametro id sea un entero
    return {"mensaje":"Usuario Encontrado",
            "Usuario":id,
            "status":200}

@app.get("/v1/usuarios/",tags=['Parametro Opcional']) #No puede haber enpoints del mismo metodo con el mismo nombre, se eliminan las llaves que especifican el parametro
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
    