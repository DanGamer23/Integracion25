package com.ferremas.API2.repository;

import com.ferremas.API2.model.Marca;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional; // <--- ¡Asegúrate de importar Optional!

@Repository
public interface MarcaRepository extends JpaRepository<Marca, Long> {
    // AÑADIR ESTE MÉTODO:
    Optional<Marca> findByNombre(String nombre);
}