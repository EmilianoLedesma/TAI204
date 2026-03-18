from fastapi import HTTPException, Depends, status, APIRouter
from app.data.database import usuarios
from app.models.usuarios import Crear_Usuario
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix = "/v1/usuarios", tags=['CRUD HTTP']
)


@router.get("/")
async def consultaT():
    return {
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

@router.post("/", status_code = status.HTTP_201_CREATED)
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