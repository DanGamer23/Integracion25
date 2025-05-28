package com.ferremas.API2.model;

import jakarta.persistence.*;

@Entity
@Table(name = "MARCA")
public class Marca {

    @Id
    @Column(name = "MARCA_ID")
    private Long id;

    @Column(name = "NOMBRE")
    private String nombre;

    // Getters y setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
}
