SET SERVEROUTPUT ON; 
ALTER SESSION SET CURRENT_SCHEMA = FERREMAS;

DROP SEQUENCE seq_usuario_id;
DROP SEQUENCE PRODUCTO_SEQ;
DROP TABLE PAGO CASCADE CONSTRAINTS;
DROP TABLE DETALLE_PEDIDO CASCADE CONSTRAINTS;
DROP TABLE PEDIDO CASCADE CONSTRAINTS;
DROP TABLE PRODUCTO CASCADE CONSTRAINTS;
DROP TABLE USUARIO CASCADE CONSTRAINTS;
DROP TABLE CATEGORIA CASCADE CONSTRAINTS;
DROP TABLE MARCA CASCADE CONSTRAINTS;
DROP TABLE ROL CASCADE CONSTRAINTS;


CREATE SEQUENCE seq_usuario_id
START WITH 6
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE SEQUENCE PRODUCTO_SEQ
START WITH 26
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE SEQUENCE seq_pedido_id
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE SEQUENCE seq_pago_id
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE SEQUENCE seq_detalle_pedido_id
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Tabla ROL
CREATE TABLE ROL (
    rol_id NUMBER(1) PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL
);

-- Tabla MARCA
CREATE TABLE MARCA (
    marca_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL
);

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    categoria_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(1000) NOT NULL
);

-- Tabla USUARIO
CREATE TABLE USUARIO (
    id_usuario NUMBER(10) PRIMARY KEY,
    rut CHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR2(100) NOT NULL,
    apellido_p VARCHAR2(100) NOT NULL,
    apellido_m VARCHAR2(100),
    snombre VARCHAR2(100),
    email VARCHAR2(100) NOT NULL UNIQUE,
    fono VARCHAR2(20),
    direccion VARCHAR2(200),
    password VARCHAR2(200) NOT NULL,
    intentos_fallidos NUMBER(2) DEFAULT 0 NOT NULL,
    bloqueado_hasta TIMESTAMP,
    rol_id number(1) NOT NULL,
    requiere_cambio_password NUMBER(1) DEFAULT 0 NOT NULL,
    CONSTRAINT USUARIO_ROL_FK FOREIGN KEY (rol_id)
	REFERENCES ROL(rol_id) ON DELETE CASCADE
);

-- Tabla PRODUCTO
CREATE TABLE PRODUCTO (
    producto_id NUMBER(10) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(300),
    precio NUMBER(10) NOT NULL,
    categoria_id NUMBER(10) NOT NULL,
    marca_id NUMBER(10) NOT NULL,
    imagen VARCHAR2(1000),
    CONSTRAINT PRODUCTO_CATEGORIA_FK FOREIGN KEY (categoria_id) 
        REFERENCES CATEGORIA(categoria_id) ON DELETE CASCADE,
    CONSTRAINT PRODUCTO_MARCA_FK FOREIGN KEY (marca_id) 
        REFERENCES MARCA(marca_id) ON DELETE CASCADE
        
);

-- Tabla PEDIDO
CREATE TABLE PEDIDO (
    pedido_id NUMBER(10) PRIMARY KEY,
    cliente_id NUMBER(10) NOT NULL,
    fecha_pedido DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(50) DEFAULT 'Pendiente' NOT NULL,
    total NUMBER(10) NOT NULL,
    vendedor_id NUMBER(10) NOT NULL,
    CONSTRAINT PEDIDO_USUARIO_FK FOREIGN KEY (cliente_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT PEDIDO_VENDEDOR_FK FOREIGN KEY (vendedor_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- Tabla DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    detalle_id NUMBER(10) PRIMARY KEY,
    pedido_id NUMBER(10) NOT NULL,
    producto_id NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    precio_unit NUMBER(10) NOT NULL,
    CONSTRAINT DETALLE_PEDIDO_PRODUCTO_FK FOREIGN KEY (producto_id) 
        REFERENCES PRODUCTO(producto_id) ON DELETE CASCADE,
    CONSTRAINT DETALLE_PEDIDO_PEDIDO_FK FOREIGN KEY (pedido_id) 
        REFERENCES PEDIDO(pedido_id) ON DELETE CASCADE
);

-- Tabla PAGO
CREATE TABLE PAGO (
    pago_id NUMBER(10) PRIMARY KEY,
    pedido_id NUMBER(10) NOT NULL,
    monto NUMBER(10) NOT NULL,
    fecha_pago DATE DEFAULT SYSDATE NOT NULL,
    contador_id NUMBER(10),
    metodo_pago VARCHAR2(50),
    estado_pago VARCHAR2(50),
    CONSTRAINT PAGO_PEDIDO_FK FOREIGN KEY (pedido_id) 
        REFERENCES PEDIDO(pedido_id) ON DELETE CASCADE,
    CONSTRAINT PAGO_USUARIO_FK FOREIGN KEY (contador_id) 
        REFERENCES USUARIO(id_usuario) ON DELETE SET NULL
);

ALTER TABLE USUARIO ADD codigo_reset VARCHAR2(10);
ALTER TABLE USUARIO ADD fecha_reset TIMESTAMP;
COMMIT;

-- Insertar datos en la tabla ROL
INSERT INTO ROL (rol_id, nombre)
VALUES (1, 'Cliente');

INSERT INTO ROL (rol_id, nombre)
VALUES (2, 'Vendedor');

INSERT INTO ROL (rol_id, nombre)
VALUES (3, 'Contador');

INSERT INTO ROL (rol_id, nombre)
VALUES (4, 'Bodeguero');

INSERT INTO ROL (rol_id, nombre)
VALUES (5, 'Administrador');


-- Insertar usuarios con rol Cliente
INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id)
VALUES (1, '12345678-9', 'Juan', 'Pérez', 'Gómez', 'Carlos', 'example@gmail.com', '987654321', 'Avenida Siempreviva 742, Santiago, Chile', '$2b$12$qs9On1lDme1MzJeDvSH9a.O0IEdCRnH1oF/t.bJBolSsahftd9MDW', 1);

-- Insertar usuarios con rol Vendedor
INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id)
VALUES (2, '34567890-1', 'Carlos', 'Gómez', 'Vega', 'Javier', 'test@hotmail.com', '923456789', 'Calle Gabriela 631, Santiago, Chile', '$2b$12$TftEZHYJxij.6oL.udQh/O42a7PJy0WObtR1cA04EMcQtQwzKaVRu', 2);

-- Insertar usuarios con rol Contador
INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id)
VALUES (3, '21727510-5', 'Pedro', 'Sánchez', 'Bravo', 'Roberto', 'ejemplo@gmail.com', '945678901', 'Los Monjes 3209, Santiago, Chile', '$2b$12$R8tr1youyhtOBRToHUp.gukks.NBj5mM0MKOx8e8U3.wcQgULlGbG', 3);

-- Insertar usuarios con rol Bodeguero
INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id)
VALUES (4, '78901234-5', 'Luis', 'Méndez', 'Ríos', 'Daniel', 'prueba@outlook.com', '967890123', 'El Virrey 1193, Santiago, Chile', '$2b$12$ALW0u60nfHZZULXcC7m4..SVki3EHCYwZ4oVNFAaV8meDhNLNUHiy', 4);

-- Insertar usuarios con rol Administrador
INSERT INTO USUARIO (id_usuario, rut, nombre, apellido_p, apellido_m, snombre, email, fono, direccion, password, rol_id, requiere_cambio_password)
VALUES (5, '56789012-3', 'Cristobal', 'Ahumada', 'Alonso', 'Vivanco', 'cris.ahumada@gmail.com', '989012345', 'Calle Concha y Toro 5020, La Serena, Chile', '$2b$12$vyMb5la6lOSBB3wOo3mhJOoignhTyqYL81ak6BUMnacw7gIXl.5cG', 5, 1);

-- Insertar datos en la tabla MARCA
INSERT INTO MARCA (marca_id, nombre) VALUES (101, 'Bosch');
INSERT INTO MARCA (marca_id, nombre) VALUES (102, 'Stanley');
INSERT INTO MARCA (marca_id, nombre) VALUES (103, 'DeWalt');
INSERT INTO MARCA (marca_id, nombre) VALUES (104, 'Makita');
INSERT INTO MARCA (marca_id, nombre) VALUES (105, 'Truper');
INSERT INTO MARCA (marca_id, nombre) VALUES (106, 'Black+Decker');
INSERT INTO MARCA (marca_id, nombre) VALUES (107, 'Bahco');
INSERT INTO MARCA (marca_id, nombre) VALUES (108, 'Milwaukee');
INSERT INTO MARCA (marca_id, nombre) VALUES (109, 'Bellota');
INSERT INTO MARCA (marca_id, nombre) VALUES (110, 'Pretul');
INSERT INTO MARCA (marca_id, nombre) VALUES (111, 'Ingco');
INSERT INTO MARCA (marca_id, nombre) VALUES (112, 'Einhell');

-- Insertar datos en la tabla CATEGORIA
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (1, 'Herramientas Manuales');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (2, 'Herramientas Eléctricas');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (3, 'Materiales Básicos');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (4, 'Acabados');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (5, 'Pinturas');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (6, 'Barnices');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (7, 'Cerámicos');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (8, 'Equipos de Seguridad');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (9, 'Tornillos y Anclajes');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (10, 'Fijaciones y Adhesivos');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (11, 'Equipos de Medición');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (12, 'Fontanería');
INSERT INTO CATEGORIA (categoria_id, nombre) VALUES (13, 'Jardinería');

-- Insertar datos en la tabla PRODUCTO
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (1, 'Martillo de Uña 16oz', 'Martillo forjado en una pieza, mango de goma antivibración. Ideal para carpintería y construcción.', 18000, 1, 102, '/static/img/productos/martillo_stanley.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (2, 'Set de Destornilladores Pro', 'Juego de 8 destornilladores de precisión con puntas imantadas y mangos ergonómicos. Incluye Phillips y Planos.', 25000, 1, 107, '/static/img/productos/destornilladores_bahco.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (3, 'Llave Ajustable Cromada 10"', 'Llave perica de alta resistencia de 10 pulgadas con mandíbula de apertura extra ancha. Acabado cromado.', 15000, 1, 105, '/static/img/productos/llave_ajustable_truper.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (4, 'Taladro Percutor 13mm', 'Potente taladro percutor de 850W, ideal para perforar concreto, metal y madera. Incluye mandril de 13mm.', 45000, 2, 101, '/static/img/productos/taladro_bosch.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (5, 'Sierra Circular 7-1/4"', 'Sierra circular de 1400W para cortes precisos en madera. Incluye hoja de carburo. Empuñadura suave.', 89000, 2, 104, '/static/img/productos/sierra_makita.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (6, 'Lijadora Orbital 1/4 Hoja', 'Lijadora de 200W para acabados finos en madera y superficies. Recolector de polvo integrado.', 32000, 2, 106, '/static/img/productos/lijadora_blackdecker.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (7, 'Cinta Adhesiva para Ductos', 'Cinta de alta resistencia para sellado de ductos y reparaciones generales. 50 metros de largo.', 5000, 10, 110, '/static/img/productos/cinta_ducto_pretul.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (8, 'Cemento Portland 25kg', 'Saco de cemento de alta calidad para obras de construcción general y albañilería.', 8000, 3, 105, '/static/img/productos/cemento_truper.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (9, 'Guantes de Seguridad Anticorte', 'Guantes de protección de nivel 5, ideales para trabajos con herramientas y materiales punzantes.', 9500, 8, 109, '/static/img/productos/guantes_bellota.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (10, 'Casco de Seguridad Industrial', 'Casco de protección rígido con ajuste de barbilla, cumple normativa ANSI Z89.1.', 22000, 8, 103, '/static/img/productos/casco_dewalt.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (11, 'Lentes de Seguridad Antiempañantes', 'Gafas de protección con tratamiento antiempañante y antirayaduras. Protección UV.', 7000, 8, 102, '/static/img/productos/lentes_stanley.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (12, 'Tornillos Madera Cabeza Plana (100u)', 'Caja de 100 tornillos para madera de 1" x 8, cabeza plana y rosca gruesa. Acabado zincado.', 4500, 9, 110, '/static/img/productos/tornillos_pretul.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (13, 'Silicona Acética Transparente', 'Sellador de silicona multiuso para baños y cocinas. Resistente al moho y la humedad. Cartucho de 300ml.', 6000, 10, 105, '/static/img/productos/silicona_truper.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (14, 'Cinta Métrica 5m Magnética', 'Cinta métrica de 5 metros con carcasa resistente y gancho magnético. Bloqueo automático.', 7000, 11, 102, '/static/img/productos/cinta_metrica_stanley.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (15, 'Nivel Láser Cruzado Auto-Nivelante', 'Nivel láser con líneas horizontales y verticales. Rango de 20 metros. Ideal para instalaciones.', 75000, 11, 101, '/static/img/productos/nivel_laser_bosch.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (16, 'Llave de Tubo Stilson 14"', 'Llave de grifa de 14 pulgadas para fontanería. Mordazas de acero de alta resistencia.', 22000, 12, 107, '/static/img/productos/llave_stilson_bahco.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (17, 'Aspersor de Riego Oscilante', 'Aspersor oscilante para riego de jardines medianos a grandes. Cobertura ajustable.', 14000, 13, 109, '/static/img/productos/aspersor_bellota.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (18, 'Pintura Blanca Lavable 1 Galón', 'Pintura látex acrílica de interior, acabado mate. Fácil de limpiar y alta cobertura.', 15000, 5, 106, '/static/img/productos/pintura_blanca_blackdecker.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (19, 'Barniz Marino Brillante 1 Litro', 'Barniz protector para madera expuesta al exterior. Resistencia a la intemperie y rayos UV.', 12000, 6, 110, '/static/img/productos/barniz_pretul.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (20, 'Cerámica de Piso 30x30cm (m2)', 'Caja de baldosas cerámicas para piso, acabado mate, resistente al desgaste. Precio por metro cuadrado.', 8000, 7, 105, '/static/img/productos/ceramica_truper.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (21, 'Ladrillo Fiscal (unidad)', 'Ladrillo de arcilla cocida, ideal para muros y construcciones tradicionales. Precio por unidad.', 300, 3, 105, '/static/img/productos/ladrillo_fiscal.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (22, 'Espátula para Masilla 4"', 'Espátula de acero inoxidable con mango de goma. Ideal para aplicar y alisar masilla y yeso.', 4000, 4, 102, '/static/img/productos/espatula_stanley.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (23, 'Rotomartillo SDS Plus', 'Rotomartillo de 900W para perforaciones de alta potencia en concreto y mampostería. 3 modos de operación.', 120000, 2, 108, '/static/img/productos/rotomartillo_milwaukee.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (24, 'Motosierra a Gasolina 50cc', 'Potente motosierra de 50cc con barra de 20 pulgadas. Ideal para cortar árboles y leña.', 200000, 2, 104, '/static/img/productos/motosierra_makita_grande.jpg');
INSERT INTO PRODUCTO (producto_id, nombre, descripcion, precio, categoria_id, marca_id, imagen)
VALUES (25, 'Juego de Brocas para Concreto', 'Set de 5 brocas SDS Plus para concreto y ladrillo. Medidas de 6mm a 12mm.', 20000, 2, 101, '/static/img/productos/brocas_concreto_bosch.jpg');

-- Pedido de prueba
INSERT INTO PEDIDO (pedido_id, cliente_id, fecha_pedido, estado, total, vendedor_id, tipo_entrega)
VALUES (100, 1, SYSDATE, 'Aprobado', 15000, 2, 'despacho');

INSERT INTO PEDIDO (pedido_id, cliente_id, fecha_pedido, estado, total, vendedor_id, tipo_entrega)
VALUES (101, 1, SYSDATE, 'Pendiente', 15000, 2, 'retiro');

INSERT INTO PAGO (pago_id, pedido_id, monto, fecha_pago, contador_id, metodo_pago, estado_pago)
VALUES (200, 100, 15000, SYSDATE, 3, 'Tarjeta de Crédito', 'Aprobado');

INSERT INTO PAGO (pago_id, pedido_id, monto, fecha_pago, contador_id, metodo_pago, estado_pago)
VALUES (201, 101, 25000, SYSDATE, null, 'Transferencia', 'Pendiente');

ALTER TABLE PRODUCTO ADD CONSTRAINT UNQ_PRODUCTO_NOMBRE UNIQUE (nombre);

ALTER TABLE PEDIDO ADD (TIPO_ENTREGA VARCHAR2(50));

ALTER TABLE PEDIDO MODIFY vendedor_id NUMBER(10) NULL;

COMMIT;

