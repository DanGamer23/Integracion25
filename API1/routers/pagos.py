from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_conexion
from fastapi import Query
from typing import List

router = APIRouter(prefix="/pagos", tags=["Pagos"])

class PagoAprobacion(BaseModel):
    estado_pago: str  # 'aprobado' o 'rechazado'
    contador_id: Optional[int] = None

@router.patch("/aprobar/{pago_id}")
def aprobar_pago(pago_id: int, datos: PagoAprobacion):
    if datos.estado_pago not in ["Aprobado", "Rechazado", "Pendiente"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    with get_conexion() as connection:
        with connection.cursor() as cursor:
            # Verificamos si el pago existe y es de tipo transferencia
            cursor.execute("""
                SELECT metodo_pago, estado_pago FROM pago WHERE pago_id = :1
            """, [pago_id])
            row = cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Pago no encontrado")

            metodo_pago, estado_actual = row

            if metodo_pago.lower() != "transferencia":
                raise HTTPException(status_code=400, detail="Solo se aprueban pagos por transferencia")

            # Actualizamos el estado del pago y asignamos el contador que lo aprobó
            cursor.execute("""
                UPDATE pago
                SET estado_pago = :1,
                    contador_id = :2
                WHERE pago_id = :3
            """, [datos.estado_pago, datos.contador_id, pago_id])

            connection.commit()

    return {
        "mensaje": "Pago actualizado",
        "pago_id": pago_id,
        "nuevo_estado": datos.estado_pago
    }

@router.get("/listar", response_model=List[dict])
def listar_pagos(estado: Optional[str] = Query(None, description="Filtrar por estado del pago")):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            if estado:
                cursor.execute("""
                    SELECT 
                        p.pago_id,
                        p.pedido_id,
                        p.metodo_pago,
                        p.estado_pago,
                        p.monto,
                        p.fecha_pago,
                        u.nombre || ' ' || u.apellido_p AS contador
                    FROM pago p
                    LEFT JOIN usuario u ON p.contador_id = u.id_usuario
                    WHERE p.estado_pago = :1
                """, [estado])
            else:
                cursor.execute("""
                    SELECT 
                        p.pago_id,
                        p.pedido_id,
                        p.metodo_pago,
                        p.estado_pago,
                        p.monto,
                        p.fecha_pago,
                        u.nombre || ' ' || u.apellido_p AS contador
                    FROM pago p
                    LEFT JOIN usuario u ON p.contador_id = u.id_usuario
                """)

            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "pago_id": row[0],
                    "pedido_id": row[1],
                    "metodo_pago": row[2],
                    "estado_pago": row[3],
                    "monto": row[4],
                    "fecha_pago": row[5],
                    "contador": row[6] or "Sin asignar"
                })
            return result