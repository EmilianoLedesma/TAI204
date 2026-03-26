from fastapi import HTTPException, Depends, status, APIRouter
from app.models.usuarios import Crear_Usuario, Actualizar_Usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix = "/v1/usuarios", tags=['CRUD HTTP']
)

@router.get("/", status_code=status.HTTP_200_OK)
async def consultar_todos(db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(queryUsuario),
        "usuarios": queryUsuario
    }

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def consultar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    return {
        "status": "200",
        "usuario": usuario
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: Crear_Usuario, db: Session = Depends(get_db)):
    usuario_nuevo = usuarioDB(nombre=usuarioP.Nombre, edad=usuarioP.Edad)
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return {
        "status": "200",
        "Mensaje": "Usuario agregado",
        "usuario": usuario_nuevo
    }

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuarioP: Crear_Usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    usuario.nombre = usuarioP.Nombre
    usuario.edad   = usuarioP.Edad
    db.commit()
    db.refresh(usuario)
    return {
        "status": "200",
        "Mensaje": "Usuario actualizado",
        "usuario": usuario
    }

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_parcial_usuario(id: int, usuarioP: Actualizar_Usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    if usuarioP.Nombre is not None:
        usuario.nombre = usuarioP.Nombre
    if usuarioP.Edad is not None:
        usuario.edad = usuarioP.Edad
    db.commit()
    db.refresh(usuario)
    return {
        "status": "200",
        "Mensaje": "Usuario actualizado parcialmente",
        "usuario": usuario
    }

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, db: Session = Depends(get_db), usuario_auth: str = Depends(verificar_peticion)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")
    db.delete(usuario)
    db.commit()
    return {
        "status": "200",
        "Mensaje": f"Usuario eliminado por {usuario_auth}",
        "id": id
    }
