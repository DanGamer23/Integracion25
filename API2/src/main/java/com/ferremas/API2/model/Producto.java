package com.ferremas.API2.model;

import jakarta.persistence.*;
import java.math.BigDecimal; // Importa BigDecimal para precios


@Entity
@Table(name = "PRODUCTO")
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "producto_seq_gen")
    @SequenceGenerator(name = "producto_seq_gen", sequenceName = "PRODUCTO_SEQ", allocationSize = 1)
    @Column(name = "PRODUCTO_ID")
    private Long id;

    @Column(name = "NOMBRE")
    private String nombre;

    @Column(name = "DESCRIPCION")
    private String descripcion;

    @Column(name = "PRECIO")
    private BigDecimal precio; 

    @Column(name = "CATEGORIA_ID")
    private Long categoriaId;

    @Column(name = "MARCA_ID")
    private Long marcaId;

    @Column(name = "IMAGEN") 
    private String imagenUrl;



    // Constructor vacío (necesario para JPA)
    public Producto() {
    }

    
    public Producto(Long id, String nombre, String descripcion, BigDecimal precio, Long categoriaId, Long marcaId, String imagenUrl) {
        this.id = id;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.precio = precio;
        this.categoriaId = categoriaId;
        this.marcaId = marcaId;
        this.imagenUrl = imagenUrl;
    }


    // --- GETTERS AND SETTERS ---

    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    public String getDescripcion() {
        return descripcion;
    }
    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public BigDecimal getPrecio() {
        return precio;
    }
    public void setPrecio(BigDecimal precio) {
        this.precio = precio;
    }

    public Long getCategoriaId() {
        return categoriaId;
    }
    public void setCategoriaId(Long categoriaId) {
        this.categoriaId = categoriaId;
    }

    public Long getMarcaId() {
        return marcaId;
    }
    public void setMarcaId(Long marcaId) {
        this.marcaId = marcaId;
    }

    public String getImagenUrl() {
        return imagenUrl;
    }
    public void setImagenUrl(String imagenUrl) {
        this.imagenUrl = imagenUrl;
    }

    @Override
    public String toString() {
        return "Producto{" +
               "id=" + id +
               ", nombre='" + nombre + '\'' +
               ", descripcion='" + descripcion + '\'' +
               ", precio=" + precio +
               ", categoriaId=" + categoriaId +
               ", marcaId=" + marcaId +
               ", imagenUrl='" + imagenUrl + '\'' +
               '}';
    }
}