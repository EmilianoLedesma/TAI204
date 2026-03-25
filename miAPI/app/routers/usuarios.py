from fastapi import HTTPException, Depends, status, APIRouter
from app.data.database import usuarios
from app.models.usuarios import Crear_Usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix = "/v1/usuarios", tags=['CRUD HTTP']
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP:Crear_Usuario, db: Session = Depends(get_db)):
    usuario_nuevo = usuarioDB(nombre=usuarioP.Nombre, edad=usuarioP.Edad)
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return {
        "status":"200",
        "Mensaje":"Usuario agregado",
        "usuario":usuarioP
    }
    

@router.put("/{id}", status_code = status.HTTP_200_OK)
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

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuario_auth: str = Depends(verificar_peticion)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "status":"200",
                "Mensaje": f"Usuario eliminado por {usuario_auth}",
                "usuario": eliminado
            }
    raise HTTPException(
        status_code=401,
        detail=f"El usuario no tiene los permisos"
    )

@router.get("/")
async def consultaT(db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).all()
    return {
        "status":"200",
        "total":len(queryUsuario),
        "usuarios":queryUsuario
    }