package com.ferremas.API2.controller;

import com.ferremas.API2.model.Producto;
import com.ferremas.API2.repository.ProductoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.util.ReflectionUtils;
import java.lang.reflect.Field;
import java.util.Map;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/productos")
public class ProductoController {
    @Autowired
    private ProductoRepository productoRepository;

    // GET: Obtener todos los productos, o una cantidad específica
    // Si se proporciona un parámetro de consulta "cantidad", se limita la cantidad de productos devueltos
    @GetMapping
    public List<Producto> obtenerProductos(@RequestParam(required = false) Optional<Integer> limit) {
        if (limit.isPresent()) {
            List<Producto> allProducts = productoRepository.findAll();
            int limitValue = limit.get();
            if (limitValue > 0 && limitValue < allProducts.size()) {
                return allProducts.subList(0, limitValue);
            } else {
                // Si el límite es inválido o mayor que el total, devolvemos todos.
                return allProducts;
            }
        } else {
            // Si el parámetro 'limit' no está presente, devolvemos todos los productos (comportamiento actual)
            return productoRepository.findAll();
        }
    }
    
    // GET: Obtener un producto por ID
    @GetMapping("/{id}")
    public Producto obtenerProductoPorId(@PathVariable Long id) {
        return productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));
    }
    // POST: Crear un nuevo producto
    @PostMapping
    public Producto crearProducto(@RequestBody Producto producto) {
        return productoRepository.save(producto);
    }
    // PUT: Actualizar un producto existente
    @PutMapping("/{id}")
    public Producto actualizarProducto(@PathVariable Long id, @RequestBody Producto productoActualizado) {
        Producto productoExistente = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));
        productoExistente.setNombre(productoActualizado.getNombre());
        productoExistente.setDescripcion(productoActualizado.getDescripcion());
        productoExistente.setPrecio(productoActualizado.getPrecio());
        productoExistente.setStock(productoActualizado.getStock());
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
