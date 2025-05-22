from fastapi import APIRouter, HTTPException
from database import get_conexion


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
    
@router.get("/{id_buscar}")
def obtener_cliente(id_buscar : str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT P_NOMBRE, S_NOMBRE, AP_PATERNO, AP_MATERNO, CORREO, TELEFONO, CONTRASENA FROM CLIENTE WHERE ID_CLIENTE = :ID_CLIENTE", {"ID_CLIENTE" : id_buscar})
        cliente = cursor.fetchone()
        cursor.close()
        cone.close()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        else:
            return {
                "ID_CLIENTE" : id_buscar,
                "P_NOMBRE" : cliente[0],
                "S_NOMBRE" : cliente[1],
                "AP_PATERNO" : cliente[2],
                "AP_MATERNO" : cliente[3],
                "CORREO" : cliente[4],
                "TELEFONO" : cliente[5],
                "CONTRASENA" : cliente[6]
            }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")
def agregar_cliente(ID_CLIENTE: str, P_NOMBRE: str, S_NOMBRE: str, AP_PATERNO: str, AP_MATERNO: str, CORREO: str, TELEFONO: int, CONTRASENA: str ):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            INSERT INTO CLIENTE
            VALUES(:ID_CLIENTE, :P_NOMBRE, :S_NOMBRE, :AP_PATERNO, :AP_MATERNO, :CORREO, :TELEFONO, :CONTRASENA)
        """,{
                "ID_CLIENTE" : ID_CLIENTE,
                "P_NOMBRE" : P_NOMBRE,
                "S_NOMBRE" : S_NOMBRE,
                "AP_PATERNO" : AP_PATERNO,
                "AP_MATERNO" : AP_MATERNO,
                "CORREO" : CORREO,
                "TELEFONO" : TELEFONO,
                "CONTRASENA" : CONTRASENA })
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Cliente registrado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_actualizar}")
def actualizar_cliente(id_actualizar:str,P_NOMBRE: str, S_NOMBRE: str, AP_PATERNO: str, AP_MATERNO: str, CORREO: str, TELEFONO: int, CONTRASENA: str ):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
                    UPDATE CLIENTE
                    SET P_NOMBRE = :P_NOMBRE, S_NOMBRE = :S_NOMBRE, AP_PATERNO = :AP_PATERNO, AP_MATERNO = :AP_MATERNO, CORREO = :CORREO, TELEFONO = :TELEFONO, CONTRASENA = :CONTRASENA
                    WHERE ID_CLIENTE = :ID_CLIENTE            
        """, {"ID_CLIENTE" : id_actualizar,
                "P_NOMBRE" : P_NOMBRE,
                "S_NOMBRE" : S_NOMBRE,
                "AP_PATERNO" : AP_PATERNO,
                "AP_MATERNO" : AP_MATERNO,
                "CORREO" : CORREO,
                "TELEFONO" : TELEFONO,
                "CONTRASENA" : CONTRASENA})
        if cursor.rowcount==0:
                    cursor.close()
                    cone.close()
                    raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Cliente actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id_eliminar}")
def eliminar_cliente(id_eliminar: str):
     try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM CLIENTE WHERE ID_CLIENTE = :ID_CLIENTE",{"ID_CLIENTE" : id_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cone.commit()
        cursor.close()
        cone.close()        
        return{"mensaje": "Cliente eliminado con éxito"}
     except Exception as ex:
          raise HTTPException(status_code=500, detail=str(ex))
     
from typing import Optional

@router.patch("/{id_actualizar}")
def actualizar_parcial(id_actualizar:str,P_NOMBRE: Optional[str]=None, S_NOMBRE: Optional[str]=None, AP_PATERNO: Optional[str]=None, AP_MATERNO: Optional[str]=None, CORREO: Optional[str]=None, TELEFONO: Optional[int]=None, CONTRASENA: Optional[str]=None ):
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"ID_CLIENTE:": id_actualizar}
        if P_NOMBRE:
            campos.append("P_NOMBRE = :P_NOMBRE")
            valores["P_NOMBRE"] = P_NOMBRE 
        if  S_NOMBRE:
            campos.append("S_NOMBRE = :S_NOMBRE")
            valores["S_NOMBRE"] = S_NOMBRE 
        if  AP_PATERNO:
            campos.append("AP_PATERNO = :AP_PATERNO")
            valores["AP_PATERNO"] = AP_PATERNO 
        if  AP_MATERNO:
            campos.append("AP_MATERNO = :AP_MATERNO")
            valores["AP_MATERNO"] = AP_MATERNO 
        if  CORREO:
            campos.append("CORREO = :CORREO")
            valores["CORREO"] = CORREO 
        if  TELEFONO:
            campos.append("TELEFONO = :TELEFONO")
            valores["TELEFONO"] = TELEFONO 
        if  CONTRASENA:
            campos.append("CONTRASENA = :CONTRASENA")
            valores["CONTRASENA"] = CONTRASENA 


        cursor.execute(f"UPDATE CLIENTE SET {', '.join(campos)} WHERE ID_CLIENTE = :ID_CLIENTE", valores )
        if cursor.rowcount==0:
            cursor.close()
            cone.close() 
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cone.commit()
        cursor.close()
        cone.close()            
        return {"mensaje": "Cliente actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))