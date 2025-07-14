from conexion import get_conexion

conn = get_conexion()
cursor = conn.cursor()
cursor.execute("SELECT SYSDATE FROM dual")
print(cursor.fetchone())
cursor.close()
conn.close()
