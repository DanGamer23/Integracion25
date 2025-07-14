from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_conexion
from fastapi import Query
from typing import List

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

class PedidoDTO(BaseModel):
    pedido_id: int
    cliente_id: int
    cliente_nombre: str
    fecha_pedido: str
    estado: str
    total: float
    vendedor_id: Optional[int] = None
    vendedor_nombre: Optional[str] = None
    tipo_entrega: Optional[str] = None


class EstadoPedido(BaseModel):
    estado: str

@router.get("/listar", response_model=List[PedidoDTO])
def listar_pedidos(estado: Optional[str] = Query(None, description="Filtrar por estado del pedido")):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            if estado:
                cursor.execute("""
                    SELECT 
                        p.pedido_id,
                        p.cliente_id,
                        c.nombre || ' ' || c.apellido_p AS cliente_nombre,
                        TO_CHAR(p.fecha_pedido, 'YYYY-MM-DD HH24:MI:SS'),
                        p.estado,
                        p.total,
                        p.vendedor_id,
                        v.nombre || ' ' || v.apellido_p AS vendedor_nombre,
                        p.tipo_entrega
                    FROM pedido p
                    JOIN usuario c ON p.cliente_id = c.id_usuario
                    LEFT JOIN usuario v ON p.vendedor_id = v.id_usuario
                    WHERE LOWER(p.estado) = LOWER(:1)
                    ORDER BY p.fecha_pedido DESC
                """, [estado])
            else:
                cursor.execute("""
                    SELECT 
                        p.pedido_id,
                        p.cliente_id,
                        c.nombre || ' ' || c.apellido_p AS cliente_nombre,
                        TO_CHAR(p.fecha_pedido, 'YYYY-MM-DD HH24:MI:SS'),
                        p.estado,
                        p.total,
                        p.vendedor_id,
                        v.nombre || ' ' || v.apellido_p AS vendedor_nombre,
                        p.tipo_entrega
                    FROM pedido p
                    JOIN usuario c ON p.cliente_id = c.id_usuario
                    LEFT JOIN usuario v ON p.vendedor_id = v.id_usuario
                    ORDER BY p.fecha_pedido DESC
                """)

            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "pedido_id": row[0],
                    "cliente_id": row[1],
                    "cliente_nombre": row[2],
                    "fecha_pedido": row[3],
                    "estado": row[4],
                    "total": float(row[5]),
                    "vendedor_id": row[6],
                    "vendedor_nombre": row[7] or "Sin asignar",
                    "tipo_entrega": row[8] or "No especificado"
                })
            return result

@router.patch("/actualizar/{pedido_id}")
def actualizar_estado_pedido(pedido_id: int, datos: EstadoPedido):
    estado_nuevo = datos.estado.lower()

    if estado_nuevo not in ["aprobado", "rechazado", "pendiente", "enviado", "entregado"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    with get_conexion() as connection:
        with connection.cursor() as cursor:
            # Validar existencia del pedido
            cursor.execute("SELECT 1 FROM pedido WHERE pedido_id = :1", [pedido_id])
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            # Buscar pago asociado
            cursor.execute("""
                SELECT metodo_pago, estado_pago
                FROM pago
                WHERE pedido_id = :1
            """, [pedido_id])
            pago = cursor.fetchone()

            if estado_nuevo == "aprobado":
                if not pago:
                    raise HTTPException(status_code=400, detail="No hay un pago asociado al pedido")

                metodo_pago, estado_pago = pago
                if metodo_pago.lower() == "transferencia" and estado_pago.lower() != "aprobado":
                    raise HTTPException(status_code=400, detail="No se puede aprobar: el pago por transferencia aún no ha sido aprobado.")

                # Si es tarjeta, se aprueba igual

            elif estado_nuevo == "rechazado":
                if pago and pago[1].lower() == "aprobado":
                    raise HTTPException(status_code=400, detail="No se puede rechazar: el pago ya fue aprobado.")

            # Actualizar estado
            cursor.execute("""
                UPDATE pedido SET estado = :1 WHERE pedido_id = :2
            """, [estado_nuevo.capitalize(), pedido_id])
            connection.commit()

    return {"mensaje": f"Estado del pedido {pedido_id} actualizado a {estado_nuevo.capitalize()}"}

@router.patch("/enviar-bodega/{pedido_id}")
def enviar_a_bodega(pedido_id: int):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT estado FROM pedido WHERE pedido_id = :1", [pedido_id])
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            estado_actual = row[0]
            if estado_actual.lower() != "aprobado":
                raise HTTPException(status_code=400, detail="Solo se pueden enviar pedidos aprobados a bodega")

            cursor.execute("""
                UPDATE pedido
                SET estado = 'En preparación'
                WHERE pedido_id = :1
            """, [pedido_id])

            connection.commit()

    return {"mensaje": "Pedido enviado a bodega"}

@router.get("/listar-en-preparacion")
def listar_en_preparacion():
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.pedido_id,
                    p.cliente_id,
                    c.nombre || ' ' || c.apellido_p AS cliente_nombre,
                    TO_CHAR(p.fecha_pedido, 'YYYY-MM-DD HH24:MI:SS'),
                    p.estado,
                    p.total,
                    p.vendedor_id,
                    v.nombre || ' ' || v.apellido_p AS vendedor_nombre,
                    p.tipo_entrega
                FROM pedido p
                JOIN usuario c ON p.cliente_id = c.id_usuario
                LEFT JOIN usuario v ON p.vendedor_id = v.id_usuario
                WHERE LOWER(p.estado) IN ('en preparación', 'preparando', 'listo')
                ORDER BY p.fecha_pedido DESC
            """)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "pedido_id": row[0],
                    "cliente_id": row[1],
                    "cliente_nombre": row[2],
                    "fecha_pedido": row[3],
                    "estado": row[4],
                    "total": float(row[5]),
                    "vendedor_id": row[6],
                    "vendedor_nombre": row[7] or "Sin asignar",
                    "tipo_entrega": row[8] or "No especificado"
                })
            return result


@router.patch("/preparar/{pedido_id}")
def aceptar_y_preparar(pedido_id: int):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE pedido SET estado = 'Preparando' WHERE pedido_id = :1 AND estado = 'En preparación'
            """, [pedido_id])
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="No se puede preparar este pedido.")
            connection.commit()
    return {"mensaje": "Pedido en preparación"}

@router.patch("/entregar-vendedor/{pedido_id}")
def entregar_a_vendedor(pedido_id: int):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE pedido SET estado = 'Listo' WHERE pedido_id = :1 AND estado = 'Preparando'
            """, [pedido_id])
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="No se puede marcar como listo.")
            connection.commit()
    return {"mensaje": "Pedido entregado al vendedor"}

@router.get("/usuario/{cliente_id}", response_model=List[PedidoDTO])
def listar_pedidos_usuario(cliente_id: int):
    with get_conexion() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.pedido_id,
                    p.cliente_id,
                    c.nombre || ' ' || c.apellido_p AS cliente_nombre,
                    TO_CHAR(p.fecha_pedido, 'YYYY-MM-DD HH24:MI:SS'),
                    p.estado,
                    p.total,
                    p.vendedor_id,
                    v.nombre || ' ' || v.apellido_p AS vendedor_nombre,
                    p.tipo_entrega
                FROM pedido p
                JOIN usuario c ON p.cliente_id = c.id_usuario
                LEFT JOIN usuario v ON p.vendedor_id = v.id_usuario
                WHERE p.cliente_id = :1
                ORDER BY p.fecha_pedido DESC
            """, [cliente_id])
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    "pedido_id": row[0],
                    "cliente_id": row[1],
                    "cliente_nombre": row[2],
                    "fecha_pedido": row[3],
                    "estado": row[4],
                    "total": float(row[5]),
                    "vendedor_id": row[6],
                    "vendedor_nombre": row[7] or "Sin asignar",
                    "tipo_entrega": row[8] or "No especificado"
                })
            return result
