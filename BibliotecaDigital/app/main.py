#importaciones
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

#intancia del servidor
app = FastAPI(
    title="Biblioteca Digital",
    description="Sistema de gestión de biblioteca digital",
    version="1.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "400", "detail": "Datos inválidos o faltantes", "errors": exc.errors()}
    )

#tablas ficticias
usuarios=[
    {"id":1, "Nombre":"Diego", "Edad":21, "Correo":"diego@gmail.com"},
    {"id":2, "Nombre":"Coral", "Edad":20, "Correo":"coral@gmail.com"},
    {"id":3, "Nombre":"Saul", "Edad":24, "Correo":"Saul@gmail.com"}
]

libros = [
    {"id":1, "Estado":"Disponible", "Nombre_del_Libro":"Mistborn: El Imperio Final", "Ano":2006, "Paginas": 557},
    {"id":2, "Estado":"Prestado", "Nombre_del_Libro":"Mistborn: El Pozo de la Ascensión", "Ano":1985, "Paginas": 348},
    {"id":3, "Estado":"Disponible", "Nombre_del_Libro":"Mistborn: El Héroe de las Eras", "Ano":1981, "Paginas": 128},
]

prestamos = [
    {"id":1, "libro_id":2, "usuario_id":1}
]

#Modelos pydantic para la validacion de datos
class Crear_Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example = "Emiliano Ledesma")
    Edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 - 125")
    Correo: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Correo electrónico válido", example = "juanito@gmail.com")

class Crear_Libro(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro")
    Estado: Literal["Disponible", "Prestado"] = Field(..., description="Estado del libro", example = "Disponible")
    Nombre_del_Libro: str = Field(..., min_length=2, max_length=100, description="Nombre del libro", example = "El Señor de los Anillos")   
    Ano: int = Field(..., gt=1450, le=datetime.now().year, description="Año entre 1451 y el año actual", example = 1954)
    Paginas: int = Field(..., gt=1, description="Número de páginas del libro")

class Crear_Prestamo(BaseModel):
    libro_id: int = Field(..., gt=0, description="ID del libro a prestar")
    usuario_id: int = Field(..., gt=0, description="ID del usuario que recibe el préstamo")

@app.get("/v1/usuarios/",tags=['Usuarios']) 
async def consultaU():
    return {
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

#endpoints - Libros
@app.get("/v1/libros/", tags=['Libros'])
async def consultaT():
    return {
        "status":"200",
        "total":len(libros),
        "libros":libros
    }
    
@app.get("/v1/libros/disponibles", tags=['Libros'])
async def libros_disponibles():
    disponibles = [li for li in libros if li["Estado"] == "Disponible"]
    return {
        "status": "200",
        "total": len(disponibles),
        "libros": disponibles
    }
    

@app.get("/v1/libros/buscar", tags=['Libros'])
async def buscar_libro(nombre: str):
    resultados = [
        li for li in libros
        if li["Nombre_del_Libro"] == nombre
    ]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontró ningún libro con ese nombre")
    return {
        "status": "200",
        "total": len(resultados),
        "libros": resultados
    }

@app.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED)
async def agregar_libro(libro: Crear_Libro):
    for li in libros:
        if li["id"] == libro.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El id ya existe")
    libros.append(libro.model_dump())
    return {
        "status":"201",
        "Mensaje":"Libro agregado",
        "libro":libro
    }


#endpoints - Usuarios
@app.post("/v1/usuarios/", tags=['Usuarios'], status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario: Crear_Usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=409, detail="El id ya existe")
    usuarios.append(usuario.model_dump())
    return {
        "status":"201",
        "Mensaje":"Usuario agregado",
        "usuario":usuario
    }

#endpoints - Prestamos
@app.get("/v1/prestamos/", tags=['Prestamos'])
async def consultar_prestamos():
    return {
        "status": "200",
        "total": len(prestamos),
        "prestamos": prestamos
    }

@app.post("/v1/prestamos/", tags=['Prestamos'], status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: Crear_Prestamo):
    libro = next((li for li in libros if li["id"] == prestamo.libro_id), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if libro["Estado"] == "Prestado":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado")

    usuario = next((u for u in usuarios if u["id"] == prestamo.usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_id = max(p["id"] for p in prestamos) + 1 if prestamos else 1
    nuevo_prestamo = {"id": nuevo_id, "libro_id": prestamo.libro_id, "usuario_id": prestamo.usuario_id}
    prestamos.append(nuevo_prestamo)
    libro["Estado"] = "Prestado"
    return {
        "status": "201",
        "Mensaje": f"Libro prestado a {usuario['Nombre']}",
        "prestamo": nuevo_prestamo
    }

@app.put("/v1/libros/{libro_id}/devolver", tags=['Libros'], status_code=status.HTTP_200_OK)
async def devolver_libro(libro_id: int):
    libro = next((li for li in libros if li["id"] == libro_id), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if libro["Estado"] == "Disponible":
        raise HTTPException(status_code=409, detail="El libro no está prestado")
    
    libro["Estado"] = "Disponible"
    return {
        "status": "200",
        "Mensaje": "Libro marcado como devuelto",
        "libro": libro
    }

@app.delete("/v1/prestamos/{prestamo_id}", tags=['Prestamos'], status_code=status.HTTP_200_OK)
async def eliminar_prestamo(prestamo_id: int):
    prestamo = next((p for p in prestamos if p["id"] == prestamo_id), None)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo no existe")

    prestamos.remove(prestamo)
    return {
        "status": "200",
        "Mensaje": "Registro de préstamo eliminado",
        "prestamo": prestamo
    }
