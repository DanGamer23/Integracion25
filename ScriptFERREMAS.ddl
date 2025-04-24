DROP TABLE ADMINISTRADOR CASCADE CONSTRAINTS 
;

DROP TABLE BODEGUERO CASCADE CONSTRAINTS 
;

DROP TABLE CARRITO CASCADE CONSTRAINTS 
;

DROP TABLE CLIENTE CASCADE CONSTRAINTS 
;

DROP TABLE CONTADOR CASCADE CONSTRAINTS 
;

DROP TABLE DETALLE_CARRITO CASCADE CONSTRAINTS 
;

DROP TABLE DETALLE_PEDIDO CASCADE CONSTRAINTS 
;

DROP TABLE ENTREGA CASCADE CONSTRAINTS 
;

DROP TABLE PAGO CASCADE CONSTRAINTS 
;

DROP TABLE PEDIDO CASCADE CONSTRAINTS 
;

DROP TABLE PRODUCTO CASCADE CONSTRAINTS 
;

DROP TABLE REPORTE_VENTAS CASCADE CONSTRAINTS 
;

DROP TABLE VENDEDOR CASCADE CONSTRAINTS 
;


CREATE TABLE ADMINISTRADOR 
    ( 
     id_admin       VARCHAR2 (50)  NOT NULL , 
     nombre_usuario VARCHAR2 (50)  NOT NULL , 
     contrasena     VARCHAR2 (20)  NOT NULL 
    ) 
;

ALTER TABLE ADMINISTRADOR 
    ADD CONSTRAINT ADMINISTRADOR_PK PRIMARY KEY ( id_admin ) ;

CREATE TABLE BODEGUERO 
    ( 
     id_bodeguero VARCHAR2 (50)  NOT NULL , 
     p_nombre     VARCHAR2 (20)  NOT NULL , 
     s_nombre     VARCHAR2 (20) , 
     ap_paterno   VARCHAR2 (20)  NOT NULL , 
     ap_materno   VARCHAR2 (20) , 
     correo       VARCHAR2 (80)  NOT NULL , 
     contrasena   VARCHAR2 (20)  NOT NULL 
    ) 
;

ALTER TABLE BODEGUERO 
    ADD CONSTRAINT BODEGUERO_PK PRIMARY KEY ( id_bodeguero ) ;

CREATE TABLE CARRITO 
    ( 
     id_carrito         VARCHAR2 (50)  NOT NULL , 
     fecha_creacion     DATE  NOT NULL , 
     CLIENTE_id_cliente VARCHAR2 (50)  NOT NULL 
    ) 
;

ALTER TABLE CARRITO 
    ADD CONSTRAINT CARRITO_PK PRIMARY KEY ( id_carrito ) ;

CREATE TABLE CLIENTE 
    ( 
     id_cliente VARCHAR2 (50)  NOT NULL , 
     p_nombre   VARCHAR2 (50)  NOT NULL , 
     s_nombre   VARCHAR2 (20) , 
     ap_paterno VARCHAR2 (20)  NOT NULL , 
     ap_materno VARCHAR2 (20) , 
     correo     VARCHAR2 (50)  NOT NULL , 
     teléfono   NUMBER (10)  NOT NULL , 
     contrasena VARCHAR2 (20)  NOT NULL 
    ) 
;

ALTER TABLE CLIENTE 
    ADD CONSTRAINT CLIENTE_PK PRIMARY KEY ( id_cliente ) ;

CREATE TABLE CONTADOR 
    ( 
     id_contador VARCHAR2 (50)  NOT NULL , 
     p_nombre    VARCHAR2 (20)  NOT NULL , 
     s_nombre    VARCHAR2 (20) , 
     ap_paterno  VARCHAR2 (20)  NOT NULL , 
     ap_materno  VARCHAR2 (20) , 
     correo      VARCHAR2 (80)  NOT NULL , 
     contrasena  VARCHAR2 (20)  NOT NULL 
    ) 
;

ALTER TABLE CONTADOR 
    ADD CONSTRAINT CONTADOR_PK PRIMARY KEY ( id_contador ) ;

CREATE TABLE DETALLE_CARRITO 
    ( 
     id_detalle           VARCHAR2 (50)  NOT NULL , 
     cantidad             NUMBER  NOT NULL , 
     CARRITO_id_carrito   VARCHAR2 (50)  NOT NULL , 
     PRODUCTO_id_producto VARCHAR2 (50)  NOT NULL 
    ) 
;

ALTER TABLE DETALLE_CARRITO 
    ADD CONSTRAINT DETALLE_CARRITO_PK PRIMARY KEY ( id_detalle ) ;

CREATE TABLE DETALLE_PEDIDO 
    ( 
     id_detalle           VARCHAR2 (50)  NOT NULL , 
     cantidad             NUMBER  NOT NULL , 
     precio               NUMBER  NOT NULL , 
     PEDIDO_id_pedido     VARCHAR2 (50)  NOT NULL , 
     PRODUCTO_id_producto VARCHAR2 (50)  NOT NULL 
    ) 
;

ALTER TABLE DETALLE_PEDIDO 
    ADD CONSTRAINT DETALLE_PEDIDO_PK PRIMARY KEY ( id_detalle ) ;

CREATE TABLE ENTREGA 
    ( 
     id_entrega             VARCHAR2 (50)  NOT NULL , 
     fecha_entrega          DATE  NOT NULL , 
     tipo_entrega           VARCHAR2 (50)  NOT NULL , 
     PEDIDO_id_pedido       VARCHAR2 (50)  NOT NULL , 
     BODEGUERO_id_bodeguero VARCHAR2 (50)  NOT NULL , 
     CONTADOR_id_contador   VARCHAR2 (50)  NOT NULL 
    ) 
;
CREATE UNIQUE INDEX ENTREGA__IDX ON ENTREGA 
    ( 
     PEDIDO_id_pedido ASC 
    ) 
;

ALTER TABLE ENTREGA 
    ADD CONSTRAINT ENTREGA_PK PRIMARY KEY ( id_entrega ) ;

CREATE TABLE PAGO 
    ( 
     id_pago              VARCHAR2 (50)  NOT NULL , 
     fecha_pago           DATE  NOT NULL , 
     monto                NUMBER  NOT NULL , 
     metodo_pago          VARCHAR2 (40)  NOT NULL , 
     PEDIDO_id_pedido     VARCHAR2 (50)  NOT NULL , 
     CONTADOR_id_contador VARCHAR2 (50)  NOT NULL 
    ) 
;
CREATE UNIQUE INDEX PAGO__IDX ON PAGO 
    ( 
     PEDIDO_id_pedido ASC 
    ) 
;

ALTER TABLE PAGO 
    ADD CONSTRAINT PAGO_PK PRIMARY KEY ( id_pago ) ;

CREATE TABLE PEDIDO 
    ( 
     id_pedido            VARCHAR2 (50)  NOT NULL , 
     fecha                DATE  NOT NULL , 
     estado               VARCHAR2 (50)  NOT NULL , 
     CLIENTE_id_cliente   VARCHAR2 (50)  NOT NULL , 
     VENDEDOR_id_vendedor VARCHAR2 (50)  NOT NULL 
    ) 
;

ALTER TABLE PEDIDO 
    ADD CONSTRAINT PEDIDO_PK PRIMARY KEY ( id_pedido ) ;

CREATE TABLE PRODUCTO 
    ( 
     id_producto VARCHAR2 (50)  NOT NULL , 
     nombre      VARCHAR2 (80)  NOT NULL , 
     descripcion VARCHAR2 (500)  NOT NULL , 
     precio      NUMBER  NOT NULL , 
     stock       NUMBER  NOT NULL 
    ) 
;

ALTER TABLE PRODUCTO 
    ADD CONSTRAINT PRODUCTO_PK PRIMARY KEY ( id_producto ) ;

CREATE TABLE REPORTE_VENTAS 
    ( 
     id_reporte             VARCHAR2 (50)  NOT NULL , 
     fecha                  DATE  NOT NULL , 
     total_ventas           NUMBER  NOT NULL , 
     ADMINISTRADOR_id_admin VARCHAR2 (50)  NOT NULL 
    ) 
;

ALTER TABLE REPORTE_VENTAS 
    ADD CONSTRAINT REPORTE_VENTAS_PK PRIMARY KEY ( id_reporte ) ;

CREATE TABLE VENDEDOR 
    ( 
     id_vendedor VARCHAR2 (50)  NOT NULL , 
     p_nombre    VARCHAR2 (20)  NOT NULL , 
     s_nombre    VARCHAR2 (20) , 
     ap_paterno  VARCHAR2 (20)  NOT NULL , 
     ap_materno  VARCHAR2 (20) , 
     correo      VARCHAR2 (80)  NOT NULL , 
     contrasena  VARCHAR2 (20)  NOT NULL 
    ) 
;

ALTER TABLE VENDEDOR 
    ADD CONSTRAINT VENDEDOR_PK PRIMARY KEY ( id_vendedor ) ;

ALTER TABLE CARRITO 
    ADD CONSTRAINT CARRITO_CLIENTE_FK FOREIGN KEY 
    ( 
     CLIENTE_id_cliente
    ) 
    REFERENCES CLIENTE 
    ( 
     id_cliente
    ) 
;

ALTER TABLE DETALLE_CARRITO 
    ADD CONSTRAINT DETALLE_CARRITO_CARRITO_FK FOREIGN KEY 
    ( 
     CARRITO_id_carrito
    ) 
    REFERENCES CARRITO 
    ( 
     id_carrito
    ) 
;

ALTER TABLE DETALLE_CARRITO 
    ADD CONSTRAINT DETALLE_CARRITO_PRODUCTO_FK FOREIGN KEY 
    ( 
     PRODUCTO_id_producto
    ) 
    REFERENCES PRODUCTO 
    ( 
     id_producto
    ) 
;

ALTER TABLE DETALLE_PEDIDO 
    ADD CONSTRAINT DETALLE_PEDIDO_PEDIDO_FK FOREIGN KEY 
    ( 
     PEDIDO_id_pedido
    ) 
    REFERENCES PEDIDO 
    ( 
     id_pedido
    ) 
;

ALTER TABLE DETALLE_PEDIDO 
    ADD CONSTRAINT DETALLE_PEDIDO_PRODUCTO_FK FOREIGN KEY 
    ( 
     PRODUCTO_id_producto
    ) 
    REFERENCES PRODUCTO 
    ( 
     id_producto
    ) 
;

ALTER TABLE ENTREGA 
    ADD CONSTRAINT ENTREGA_BODEGUERO_FK FOREIGN KEY 
    ( 
     BODEGUERO_id_bodeguero
    ) 
    REFERENCES BODEGUERO 
    ( 
     id_bodeguero
    ) 
;

ALTER TABLE ENTREGA 
    ADD CONSTRAINT ENTREGA_CONTADOR_FK FOREIGN KEY 
    ( 
     CONTADOR_id_contador
    ) 
    REFERENCES CONTADOR 
    ( 
     id_contador
    ) 
;

ALTER TABLE ENTREGA 
    ADD CONSTRAINT ENTREGA_PEDIDO_FK FOREIGN KEY 
    ( 
     PEDIDO_id_pedido
    ) 
    REFERENCES PEDIDO 
    ( 
     id_pedido
    ) 
;

ALTER TABLE PAGO 
    ADD CONSTRAINT PAGO_CONTADOR_FK FOREIGN KEY 
    ( 
     CONTADOR_id_contador
    ) 
    REFERENCES CONTADOR 
    ( 
     id_contador
    ) 
;

ALTER TABLE PAGO 
    ADD CONSTRAINT PAGO_PEDIDO_FK FOREIGN KEY 
    ( 
     PEDIDO_id_pedido
    ) 
    REFERENCES PEDIDO 
    ( 
     id_pedido
    ) 
;

ALTER TABLE PEDIDO 
    ADD CONSTRAINT PEDIDO_CLIENTE_FK FOREIGN KEY 
    ( 
     CLIENTE_id_cliente
    ) 
    REFERENCES CLIENTE 
    ( 
     id_cliente
    ) 
;

ALTER TABLE PEDIDO 
    ADD CONSTRAINT PEDIDO_VENDEDOR_FK FOREIGN KEY 
    ( 
     VENDEDOR_id_vendedor
    ) 
    REFERENCES VENDEDOR 
    ( 
     id_vendedor
    ) 
;

ALTER TABLE REPORTE_VENTAS 
    ADD CONSTRAINT REPO_VENTAS_ADMIN_FK FOREIGN KEY 
    ( 
     ADMINISTRADOR_id_admin
    ) 
    REFERENCES ADMINISTRADOR 
    ( 
     id_admin
    ) 
;

INSERT INTO ADMINISTRADOR (id_admin, nombre_usuario, contrasena)
VALUES (1, 'LuisValdivia', '12345678-9');


