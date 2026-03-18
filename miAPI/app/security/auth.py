from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets #para contraseñas, hashes y ese pedo
#Seguridad de endpoints con HTTPBasic
from fastapi import HTTPException, Depends, status

Security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(Security)):
    usuario_auth = secrets.compare_digest(credenciales.username,"emiliano")
    contra_auth = secrets.compare_digest(credenciales.password, "123456")
    
    if not(usuario_auth and contra_auth):
        raise HTTPException(
                status_code= 401,
                detail= "Credenciales no autorizadas"
                )
    
    return credenciales.username