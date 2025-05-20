import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="FERREMAS",
        password="FERREMAS",
        dsn="localhost:1521/XEPDB1"
    )
    return conexion