package com.ferremas.API2.repository;

import com.ferremas.API2.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long>, JpaSpecificationExecutor<Producto> {
    // Este repositorio hereda de JpaRepository y JpaSpecificationExecutor para proporcionar
    // funcionalidades básicas de CRUD y especificaciones de consultas avanzadas.
    // Aquí puedes agregar métodos personalizados si es necesario
    List<Producto>findByCategoriaId(Long categoriaId);
    List<Producto> findByMarcaId(Long marcaId);
    List<Producto> findByNombreContainingIgnoreCase(String nombre); // Método para buscar productos por nombre (sin distinción de mayúsculas y minúsculas)
    List<Producto> findByCategoriaIdAndMarcaId(Long categoriaId, Long marcaId); // Método para buscar productos por categoría y marca
}

