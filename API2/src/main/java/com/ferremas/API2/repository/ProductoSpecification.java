package com.ferremas.API2.repository;

import com.ferremas.API2.model.Producto;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;

public class ProductoSpecification {

    // Búsqueda por palabra clave (en nombre o descripción)
    public static Specification<Producto> byKeyword(String keyword) {
        return (root, query, criteriaBuilder) -> {
            if (keyword == null || keyword.trim().isEmpty()) {
                return criteriaBuilder.conjunction(); // Condición "siempre verdadera" si no hay keyword
            }
            String lowerCaseKeyword = "%" + keyword.toLowerCase() + "%";
            return criteriaBuilder.or(
                criteriaBuilder.like(criteriaBuilder.lower(root.get("nombre")), lowerCaseKeyword),
                criteriaBuilder.like(criteriaBuilder.lower(root.get("descripcion")), lowerCaseKeyword)
            );
        };
    }

    // Filtro por ID de categoría (usando el campo categoriaId en Producto)
    public static Specification<Producto> byCategoriaId(Long categoriaId) {
        return (root, query, criteriaBuilder) -> {
            if (categoriaId == null) {
                return criteriaBuilder.conjunction();
            }
            return criteriaBuilder.equal(root.get("categoriaId"), categoriaId);
        };
    }

    // Filtro por ID de marca (usando el campo marcaId en Producto)
    public static Specification<Producto> byMarcaId(Long marcaId) {
        return (root, query, criteriaBuilder) -> {
            if (marcaId == null) {
                return criteriaBuilder.conjunction();
            }
            return criteriaBuilder.equal(root.get("marcaId"), marcaId);
        };
    }

    // Filtro por rango de precios
    public static Specification<Producto> byPriceRange(Double minPrecio, Double maxPrecio) {
        return (root, query, criteriaBuilder) -> {
            List<Predicate> predicates = new ArrayList<>();
            if (minPrecio != null && minPrecio >= 0) {
                predicates.add(criteriaBuilder.greaterThanOrEqualTo(root.get("precio"), minPrecio));
            }
            if (maxPrecio != null && maxPrecio >= 0) { // Considerar si 0 es un límite inferior o superior válido
                predicates.add(criteriaBuilder.lessThanOrEqualTo(root.get("precio"), maxPrecio));
            }
            return criteriaBuilder.and(predicates.toArray(new Predicate[0]));
        };
    }

    // Método combinado para aplicar múltiples filtros
    public static Specification<Producto> withFilters(
            String keyword,
            Long categoriaId,
            Long marcaId,
            Double minPrecio,
            Double maxPrecio) {

        Specification<Producto> spec = Specification.where(null); // Inicia con una especificación que siempre es verdadera

        // Aplica cada filtro si está presente
        spec = spec.and(byKeyword(keyword));
        spec = spec.and(byCategoriaId(categoriaId));
        spec = spec.and(byMarcaId(marcaId));
        spec = spec.and(byPriceRange(minPrecio, maxPrecio));

        return spec;
    }
}