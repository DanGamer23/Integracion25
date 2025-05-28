package com.ferremas.API2.repository;

import com.ferremas.API2.model.Categoria;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional; // <--- ¡Asegúrate de importar Optional!

@Repository
public interface CategoriaRepository extends JpaRepository<Categoria, Long> {
    // AÑADIR ESTE MÉTODO:
    Optional<Categoria> findByNombre(String nombre);
}