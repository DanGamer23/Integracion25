package com.ferremas.API2.controller;

import com.ferremas.API2.model.Categoria;
import com.ferremas.API2.repository.CategoriaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/categorias")
public class CategoriaController {

    @Autowired
    private CategoriaRepository categoriaRepository;

    @GetMapping // Maneja GET a /categorias
    public List<Categoria> getAllCategorias() {
        return categoriaRepository.findAll();
    }
}