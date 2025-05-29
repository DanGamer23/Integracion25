SET ECHO ON;
SET FEEDBACK ON;
SET SERVEROUTPUT ON;
--ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;
--CREATE USER FERREMAS IDENTIFIED BY FERREMAS;
--GRANT CONNECT, RESOURCE, DBA TO FERREMAS;

-- 01_create_ferremas_user.sql

-- Activar la salida para ver los mensajes de DBMS_OUTPUT
SET SERVEROUTPUT ON;

-- Necesario para crear usuarios locales en un PDB (en Oracle 12c+ Multitenant)
ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;

-- *** CLAVE: Conectarse al PDB XEPDB1 para asegurar que las operaciones afecten a este PDB ***
ALTER SESSION SET CONTAINER = XEPDB1;

-- Verifica si el usuario FERREMAS ya existe antes de crearlo o recrearlo
DECLARE
    user_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO user_exists FROM ALL_USERS WHERE USERNAME = 'FERREMAS';

    IF user_exists > 0 THEN
        -- Si el usuario existe, se recomienda borrarlo para una recreación limpia en desarrollo.
        -- Esto es útil para asegurar que no hay problemas de permisos o contraseña de intentos anteriores.
        DBMS_OUTPUT.PUT_LINE('Usuario FERREMAS ya existe. Intentando borrarlo y recrearlo...');
        BEGIN
            EXECUTE IMMEDIATE 'DROP USER FERREMAS CASCADE'; -- CASCADE borra también los objetos del esquema
            DBMS_OUTPUT.PUT_LINE('Usuario FERREMAS borrado.');
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('Error al borrar usuario FERREMAS (puede que tenga sesiones activas o dependencias). Error: ' || SQLERRM);
                -- Puedes decidir si quieres continuar o abortar aquí. Para desarrollo, a menudo se continúa.
        END;
    END IF;

    -- Crear el usuario
    DBMS_OUTPUT.PUT_LINE('Creando usuario FERREMAS con contraseña FERREMAS...');
    EXECUTE IMMEDIATE 'CREATE USER FERREMAS IDENTIFIED BY FERREMAS';
    DBMS_OUTPUT.PUT_LINE('Usuario FERREMAS creado.');

    -- Otorgar los permisos necesarios
    DBMS_OUTPUT.PUT_LINE('Otorgando permisos a FERREMAS...');
    EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE, DBA TO FERREMAS';
    EXECUTE IMMEDIATE 'ALTER USER FERREMAS QUOTA UNLIMITED ON USERS';
    DBMS_OUTPUT.PUT_LINE('Permisos otorgados y cuota definida para FERREMAS.');

    -- Asegurarse de que la cuenta no esté bloqueada ni expirada (aunque normalmente no lo estaría recién creada)
    EXECUTE IMMEDIATE 'ALTER USER FERREMAS ACCOUNT UNLOCK';
    EXECUTE IMMEDIATE 'ALTER USER FERREMAS PASSWORD EXPIRE'; -- Opcional: forzar cambio en el primer login
    DBMS_OUTPUT.PUT_LINE('Usuario FERREMAS desbloqueado.');

    COMMIT; -- Asegurar que los cambios se guarden
    DBMS_OUTPUT.PUT_LINE('Configuración del usuario FERREMAS completada.');

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('!!! ERROR FATAL en 01_create_ferremas_user.sql: ' || SQLERRM);
        ROLLBACK; -- Deshacer cambios si hay un error
        RAISE; -- Re-lanzar el error para que Docker lo capture
END;
/
