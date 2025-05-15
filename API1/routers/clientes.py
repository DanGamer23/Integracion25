from fastapi import APIRouter, HTTPException
from API1.database import get_conexion


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.get("/")
def obtener_clientes():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT ID_CLIENTE, P_NOMBRE, S_NOMBRE, AP_PATERNO, AP_MATERNO, CORREO, TELEFONO, CONTRASENA FROM CLIENTE")
        clientes = []
        for ID_CLIENTE, P_NOMBRE, S_NOMBRE, AP_PATERNO, AP_MATERNO, CORREO, TELEFONO, CONTRASENA in cursor:
            clientes.append({
                "ID_CLIENTE" : ID_CLIENTE,
                "P_NOMBRE" : P_NOMBRE,
                "S_NOMBRE" : S_NOMBRE,
                "AP_PATERNO" : AP_PATERNO,
                "AP_MATERNO" : AP_MATERNO,
                "CORREO" : CORREO,
                "TELEFONO" : TELEFONO,
                "CONTRASENA" : CONTRASENA
            })
        cursor.close()
        cone.close()
        return clientes
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))