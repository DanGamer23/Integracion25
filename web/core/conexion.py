import oracledb

def get_conexion():
    return oracledb.connect(
        user="FERREMAS",
        password="FERREMAS",
        dsn="oracle-db:1521/XEPDB1"
    )

if __name__ == "__main__":
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT SYSDATE FROM dual")
    print(cursor.fetchone())
    cursor.close()
    conn.close()
