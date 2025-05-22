package com.ferremas.API2.repository;

import com.ferremas.API2.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    // Aquí puedes agregar métodos personalizados si es necesario
}

