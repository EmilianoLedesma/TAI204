#importaciones
from fastapi import FastAPI
import asyncio
#intancia del servidor
app = FastAPI()

#endpoints
@app.get("/")
async def bienvenida():
    return {"mensaje":"Bienvenido a FastAPI"} #Primero la clave (como si fuera el index) y luego el valor de la clave (en este caso el mensaje a entregar)

@app.get("/holaMundo")
async def hola():
    await asyncio.sleep(5) #peticion, consulta BD, Archivo 
    return {
        "mensaje":"Hola Mundo!",
        "Status":"200"
    }