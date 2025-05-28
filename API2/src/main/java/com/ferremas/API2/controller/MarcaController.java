package com.ferremas.API2.controller;

import com.ferremas.API2.model.Marca;
import com.ferremas.API2.repository.MarcaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/marcas") 
public class MarcaController {

    @Autowired
    private MarcaRepository marcaRepository;

    @GetMapping // Maneja GET a /marcas
    public List<Marca> getAllMarcas() {
        return marcaRepository.findAll();
    }
}