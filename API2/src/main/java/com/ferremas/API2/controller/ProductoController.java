package com.ferremas.API2.controller;

import com.ferremas.API2.model.Producto;
import com.ferremas.API2.model.ProductoDTO;
import com.ferremas.API2.model.Categoria;
import com.ferremas.API2.model.Marca;
import com.ferremas.API2.repository.CategoriaRepository;
import com.ferremas.API2.repository.MarcaRepository;
import com.ferremas.API2.repository.ProductoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.util.ReflectionUtils;
import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import static com.ferremas.API2.repository.ProductoSpecification.withFilters;

@CrossOrigin(origins = "http://localhost:8001")
@RestController
@RequestMapping("/productos")
public class ProductoController {
    
    @Autowired
    private ProductoRepository productoRepository;

    @Autowired
    private CategoriaRepository categoriaRepository;

    @Autowired
    private MarcaRepository marcaRepository;

    // GET: Obtener todos los productos, o una cantidad específica
    // Si se proporciona un parámetro de consulta "limit", se limita la cantidad de productos devueltos
@GetMapping
public List<ProductoDTO> obtenerProductos(@RequestParam(required = false) Optional<Integer> limit) {
    List<Producto> productos = productoRepository.findAll();

    if (limit.isPresent()) {
        int limitValue = limit.get();
        if (limitValue > 0 && limitValue < productos.size()) {
            productos = productos.subList(0, limitValue);
        }
    }

    return productos.stream().map(producto -> {
        ProductoDTO dto = new ProductoDTO();
        dto.setId(producto.getId());
        dto.setNombre(producto.getNombre());
        dto.setDescripcion(producto.getDescripcion());
        dto.setPrecio(producto.getPrecio());
        dto.setImagenUrl(producto.getImagenUrl());

        categoriaRepository.findById(producto.getCategoriaId())
            .ifPresent(c -> dto.setCategoriaNombre(c.getNombre()));
        marcaRepository.findById(producto.getMarcaId())
            .ifPresent(m -> dto.setMarcaNombre(m.getNombre()));

        return dto;
    }).collect(Collectors.toList());
}


    // GET: Buscar productos con filtros avanzados
    @GetMapping("/filter")
    public ResponseEntity<Page<ProductoDTO>> obtenerProductosFiltrados(
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String categoriaNombre,
            @RequestParam(required = false) String marcaNombre,
            @RequestParam(required = false) Double minPrecio,
            @RequestParam(required = false) Double maxPrecio,
            @RequestParam(required = false) Long excludeId,
            Pageable pageable) {

        Long categoriaId = null;
        if (categoriaNombre != null && !categoriaNombre.isEmpty()) {
            Optional<Categoria> categoriaOpt = categoriaRepository.findByNombre(categoriaNombre);
            if (categoriaOpt.isPresent()) {
                categoriaId = categoriaOpt.get().getId();
            } else {
                return new ResponseEntity<>(Page.empty(), HttpStatus.OK);
            }
        }

        Long marcaId = null;
        if (marcaNombre != null && !marcaNombre.isEmpty()) {
            Optional<Marca> marcaOpt = marcaRepository.findByNombre(marcaNombre);
            if (marcaOpt.isPresent()) {
                marcaId = marcaOpt.get().getId();
            } else {
                return new ResponseEntity<>(Page.empty(), HttpStatus.OK);
            }
        }

        Specification<Producto> finalSpec = withFilters(search, categoriaId, marcaId, minPrecio, maxPrecio, excludeId);

        Page<Producto> productoPage = productoRepository.findAll(finalSpec, pageable);

        List<ProductoDTO> productoDTOs = productoPage.getContent().stream()
            .map(producto -> {
                ProductoDTO dto = new ProductoDTO();
                dto.setId(producto.getId());
                dto.setNombre(producto.getNombre());
                dto.setDescripcion(producto.getDescripcion());
                dto.setPrecio(producto.getPrecio());
                dto.setImagenUrl(producto.getImagenUrl());

                categoriaRepository.findById(producto.getCategoriaId())
                    .ifPresent(c -> dto.setCategoriaNombre(c.getNombre()));
                marcaRepository.findById(producto.getMarcaId())
                    .ifPresent(m -> dto.setMarcaNombre(m.getNombre()));
                return dto;
            })
            .collect(Collectors.toList());

        Page<ProductoDTO> productoDTOPage = new PageImpl<>(productoDTOs, pageable, productoPage.getTotalElements());

        return new ResponseEntity<>(productoDTOPage, HttpStatus.OK);
    }


    // GET: Buscar productos por categoría
    @GetMapping("/categoria/{categoriaId}")
    public List<Producto> obtenerProductosPorCategoria(@PathVariable Long categoriaId) {
        return productoRepository.findByCategoriaId(categoriaId);
    }

    // GET: Buscar productos por marca
    @GetMapping("/marca/{marcaId}")
    public List<Producto> obtenerProductosPorMarca(@PathVariable Long marcaId) {
        return productoRepository.findByMarcaId(marcaId);
    }

    // GET: Buscar productos por nombre (sin distinción de mayúsculas y minúsculas)
    @GetMapping("/buscar")
    public List<Producto> buscarProductosPorNombre(@RequestParam String nombre) {
        return productoRepository.findByNombreContainingIgnoreCase(nombre);
    }

    // GET: Buscar productos por categoría y marca
    @GetMapping("/categoria/{categoriaId}/marca/{marcaId}") 
    public List<Producto> obtenerProductosPorCategoriaYMarca(@PathVariable Long categoriaId, @PathVariable Long marcaId) {
        return productoRepository.findByCategoriaIdAndMarcaId(categoriaId, marcaId);
    }



    

    // GET: Obtener un producto por ID, incluyendo detalles de categoría y marca
    @GetMapping("/{id}")
    public ProductoDTO obtenerProductoPorId(@PathVariable Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));

        ProductoDTO dto = new ProductoDTO();
        dto.setId(producto.getId());
        dto.setNombre(producto.getNombre());
        dto.setDescripcion(producto.getDescripcion());
        dto.setPrecio(producto.getPrecio());
        dto.setImagenUrl(producto.getImagenUrl());

        categoriaRepository.findById(producto.getCategoriaId())
            .ifPresent(c -> dto.setCategoriaNombre(c.getNombre()));
        marcaRepository.findById(producto.getMarcaId())
            .ifPresent(m -> dto.setMarcaNombre(m.getNombre()));

        return dto;
    }

    // POST: Crear un nuevo producto
    @PostMapping
    public Producto crearProducto(@RequestBody Producto producto) {
        return productoRepository.save(producto);
    }

    // PUT: Actualizar un producto existente (actualización completa)
    @PutMapping("/{id}")
    public Producto actualizarProducto(@PathVariable Long id, @RequestBody Producto productoActualizado) {
        Producto productoExistente = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));

        productoExistente.setNombre(productoActualizado.getNombre());
        productoExistente.setDescripcion(productoActualizado.getDescripcion());
        productoExistente.setPrecio(productoActualizado.getPrecio());
        productoExistente.setCategoriaId(productoActualizado.getCategoriaId());
        productoExistente.setMarcaId(productoActualizado.getMarcaId());
        productoExistente.setImagenUrl(productoActualizado.getImagenUrl());

        return productoRepository.save(productoExistente);
    }

    // PATCH: Actualizar parcialmente un producto existente
    @PatchMapping("/{id}")
    public Producto actualizarProductoParcial(@PathVariable Long id, @RequestBody Map<String, Object> campos) {
        Producto productoExistente = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));

        campos.forEach((key, value) -> {
            Field field = ReflectionUtils.findField(Producto.class, key);
            if (field != null) {
                field.setAccessible(true); 
                ReflectionUtils.setField(field, productoExistente, value);
            }
        });

        return productoRepository.save(productoExistente);
    }

    // DELETE: Eliminar un producto por ID
    @DeleteMapping("/{id}")
    public void eliminarProducto(@PathVariable Long id) {
        Producto productoExistente = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));
        productoRepository.delete(productoExistente);
    }
}