#Para los modelos de validaciones se recomienda que el modelo se llame como la entidad principal que protege
from pydantic import BaseModel #importacion para la validacion de datos, se crea una clase que hereda de BaseModel y se definen los campos que se esperan recibir en el endpoint, con su tipo de dato correspondiente
from pydantic import Field #importacion para agregar validaciones adicionales a los campos del modelo, como longitud mínima, máxima, expresiones regulares, etc.

class Crear_Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example = "Emiliano Ledesma")
    Edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 - 125")