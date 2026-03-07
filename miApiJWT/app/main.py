#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError

#configuracion OAuth2
SECRET_KEY = "2d2cc951eb72e2470fffb6c8ce458483bf35956153223935"
ALGORITHM  = "HS256"
TOKEN_EXPIRE_MINUTES = 30

#instancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="Emiliano Ledesma",
    version="2.0"
)

#esquema OAuth2, apunta al endpoint que genera el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

#tabla ficticia
usuarios = [
    {"id": 1, "Nombre": "Diego", "Edad": 21},
    {"id": 2, "Nombre": "Coral", "Edad": 20},
    {"id": 3, "Nombre": "Saul",  "Edad": 24},
]

#Modelo pydantic para la validacion de datos
class Crear_Usuario(BaseModel):
    id:     int = Field(..., gt=0,         description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Emiliano Ledesma")
    Edad:   int = Field(..., ge=1, le=125, description="Edad valida entre 1 - 125")


#generacion del token con limite de 30 minutos
def crear_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


#validacion del token, reemplaza a verificar_peticion
def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado",
                            headers={"WWW-Authenticate": "Bearer"})


#endpoint que recibe usuario+password y regresa el token
@app.post("/auth/token", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "emiliano" or form_data.password != "123456":
        raise HTTPException(status_code=401, detail="Credenciales incorrectas",
                            headers={"WWW-Authenticate": "Bearer"})
    token = crear_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


#endpoints
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags=['Asincronia'])
async def hola():
    await asyncio.sleep(5)
    return {"mensaje": "Hola Mundo!", "Status": "200"}

@app.get("/v1/ParametroOB/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id: int):
    return {"mensaje": "Usuario Encontrado", "Usuario": id, "status": 200}

@app.get("/v1/ParametrosOp/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"Mensaje": "Usuario Encontrado", "Usuario": usuariok, "status": "200"}
        return {"Mensaje": "Usuario No encontrado", "status": "404"}
    else:
        return {"Mensaje": "No se proporciono id", "status": "204"}

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return {"status": "200", "total": len(usuarios), "usuarios": usuarios}

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregar_usuario(usuario: Crear_Usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {"status": "200", "Mensaje": "Usuario agregado", "usuario": usuario}

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario: dict, usuario_auth: str = Depends(verificar_token)):
    for usr in usuarios:
        if usr["id"] == usuario["id"]:
            usr["Nombre"] = usuario["Nombre"]
            usr["Edad"]   = usuario["Edad"]
            return {"status": "200", "Mensaje": f"Usuario actualizado por {usuario_auth}", "usuario": usr}
    raise HTTPException(status_code=404, detail=f"El usuario con id {usuario['id']} no existe")

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, usuario_auth: str = Depends(verificar_token)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {"status": "200", "Mensaje": f"Usuario eliminado por {usuario_auth}", "usuario": eliminado}
    raise HTTPException(status_code=404, detail=f"El usuario con id {id} no existe")