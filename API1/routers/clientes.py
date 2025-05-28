from typing import Optional
from fastapi import APIRouter, HTTPException
from database import get_conexion
from passlib.hash import bcrypt

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.get("/")
def obtener_usuarios():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""SELECT 
                       id_usuario,
                       rut,
                       nombre,
                       apellido_p,
                       apellido_m,
                       snombre,
                       email,
                       fono,
                       direccion,
                       password,
                       rol_id 
                       FROM USUARIO""")
        usuarios = []
        for (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password_hash, rol_id) in cursor:
            usuarios.append({
            "id_usuario": id_usuario,
            "rut": rut,
            "nombre": nombre,
            "apellido_p": apellido_p,
            "apellido_m": apellido_m,
            "snombre": snombre,
            "email": email,
            "fono": fono,
            "direccion": direccion,
            "password": password_hash,
            "rol_id": rol_id
            })
        cursor.close()
        cone.close()
        return usuarios
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_buscar}")
def obtener_usuario(id_buscar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""SELECT 
                       id_usuario,
                       rut,
                       nombre,
                       apellido_p,
                       apellido_m,
                       snombre,
                       email,
                       fono,
                       direccion,
                       password,
                       rol_id 
                       FROM USUARIO WHERE id_usuario = :id_usuario""", {"id_usuario": id_buscar})
        usuario = cursor.fetchone()
        cursor.close()
        cone.close()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id_usuario": id_buscar,
            "rut": usuario[1],
            "nombre": usuario[2],
            "apellido_p": usuario[3],
            "apellido_m": usuario[4],
            "snombre": usuario[5],
            "email": usuario[6],
            "fono": usuario[7],
            "direccion": usuario[8],
            "password": usuario[9],
            "rol_id": usuario[10]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")
def agregar_usuario(rut:str, nombre:str, apellido_p:str, apellido_m:str, snombre:str, email:str, fono:str, direccion:str, password:str,):
    try:
        # Hash the password before storing it
        hashed_password = bcrypt.hash(password)
        rol_id=1
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""INSERT INTO USUARIO 
                       VALUES 
                       (seq_usuario.nextval, 
                       :rut, 
                       :nombre, 
                       :apellido_p, 
                       :apellido_m, 
                       :snombre, 
                       :email, 
                       :fono, 
                       :direccion, 
                       :password, 
                       :rol_id)""",{
                           "rut": rut,
                           "nombre": nombre,
                           "apellido_p": apellido_p,
                           "apellido_m": apellido_m,
                           "snombre": snombre,
                           "email": email,
                           "fono": fono,
                           "direccion": direccion,
                           "password": hashed_password,
                           "rol_id": rol_id,
                       })
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Uusuario agregado correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.put("/{id_actualizar}")
def actualizar_usuario(id_actualizar:int, rut:str, nombre:str, apellido_p:str, apellido_m:str, snombre:str, email:str, fono:str, direccion:str, password:str, rol_id:int):
    try:
        # Hash the password before updating it
        hashed_password = bcrypt.hash(password)
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            UPDATE USUARIO 
            SET rut = :rut,
                nombre = :nombre,
                apellido_p = :apellido_p,
                apellido_m = :apellido_m,
                snombre = :snombre,
                email = :email,
                fono = :fono,
                direccion = :direccion,
                password = :password,
                rol_id = :rol_id
            WHERE id_usuario = :id_usuario
        """, {
            "rut": rut,
            "nombre": nombre,
            "apellido_p": apellido_p,
            "apellido_m": apellido_m,
            "snombre": snombre,
            "email": email,
            "fono": fono,
            "direccion": direccion,
            "password": hashed_password,
            "rol_id": rol_id,
            "id_usuario": id_actualizar
        })
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.delete("/{id_eliminar}")
def eliminar_usuario(id_eliminar:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""DELETE FROM USUARIO 
                       WHERE id_usuario = :id_usuario""", 
                       {"id_usuario": id_eliminar})
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario eliminado correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.patch("/{id_actualizar}")
def actualizar_patch(id_actualizar:int, rut:Optional[str]=None, nombre:Optional[str]=None, apellido_p:Optional[str]=None, apellido_m:Optional[str]=None, snombre:Optional[str]=None, email:Optional[str]=None, fono:Optional[str]=None, direccion:Optional[str]=None, password:Optional[str]=None, rol_id:Optional[int]=None):
    try:
        if not rut and not nombre and not apellido_p and not apellido_m and not snombre and not email and not fono and not direccion and not password and not rol_id:
            raise HTTPException(status_code=400, detail="No se han proporcionado datos para actualizar")
        cone = get_conexion()
        cursor = cone.cursor()
        campos=[]
        valores={"id_usuario": id_actualizar}
        if rut:
            campos.append("rut = :rut")
            valores["rut"] = rut
        if nombre:
            campos.append("nombre = :nombre")
            valores["nombre"] = nombre
        if apellido_p:
            campos.append("apellido_p = :apellido_p")
            valores["apellido_p"] = apellido_p
        if apellido_m:
            campos.append("apellido_m = :apellido_m")
            valores["apellido_m"] = apellido_m
        if snombre:
            campos.append("snombre = :snombre")
            valores["snombre"] = snombre
        if email:
            campos.append("email = :email")
            valores["email"] = email
        if fono:    
            campos.append("fono = :fono")
            valores["fono"] = fono
        if direccion:
            campos.append("direccion = :direccion")
            valores["direccion"] = direccion
        if password:
            campos.append("password = :password")
            valores["password"] = bcrypt.hash(password)
        if rol_id:
            campos.append("rol_id = :rol_id")
            valores["rol_id"] = rol_id
        cursor.execute(F"""
            UPDATE USUARIO 
            SET {', '.join(campos)}
            WHERE id_usuario = :id_usuario
        """,valores)
        if cursor.rowcount == 0:
            cone.close()
            cursor.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/login")
def login(email:str, password:str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        cursor.execute("""
            SELECT 
                id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id
            FROM USUARIO
            WHERE email = :email
        """, {"email": email,})
        usuario = cursor.fetchone()
        cursor.close()
        cone.close()
        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        stored_password_hash = usuario[9]
        if not bcrypt.verify(password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        return {
            "id_usuario": usuario[0],
            "rut": usuario[1],
            "nombre": usuario[2],
            "apellido_p": usuario[3],
            "apellido_m": usuario[4],
            "snombre": usuario[5],
            "email": usuario[6],
            "fono": usuario[7],
            "direccion": usuario[8],
            "rol_id": usuario[10]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
