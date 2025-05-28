// web/static/js/shop_products.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Referencias a elementos del DOM ---
    const shopProductsContainer = document.getElementById('shop-products-container');
    const categoryFilterList = document.getElementById('category-filter-list');
    const brandFilterList = document.getElementById('brand-filter-list');
    const searchKeywordsInput = document.getElementById('search-keywords');
    const searchButton = document.getElementById('search-button');
    const minPriceInput = document.getElementById('min-price');
    const maxPriceInput = document.getElementById('max-price');
    const applyPriceFilterButton = document.getElementById('apply-price-filter');
    const sortingDropdown = document.getElementById('sorting-dropdown');
    const paginationControls = document.getElementById('pagination-controls');

    // ** IMPORTANTE: URL base de tu API de Spring Boot **
    const apiBaseUrl ='http://127.0.0.1:8080'; 

    // --- Estado de los filtros y paginación ---
    let currentFilters = {
        search: '',
        categoryName: '', // Usaremos el nombre de la categoría
        brandName: '',    // Usaremos el nombre de la marca
        minPrecio: 0,
        maxPrecio: 9999999, // Un valor grande por defecto
        sortBy: '',       // Campo y dirección de ordenación (ej: 'nombre,asc')
        page: 0,          // Página actual (0-based indexing para Spring Data JPA)
        size: 8           // Cantidad de productos por página
    };

    // --- Funciones de Utilidad ---

    // Formatea el precio a CLP
    function formatPrice(price) {
        return new Intl.NumberFormat('es-CL', { 
            style: 'currency', 
            currency: 'CLP', 
            minimumFractionDigits: 0 
        }).format(price);
    }

    // Muestra un mensaje de carga
    function showLoading() {
        shopProductsContainer.innerHTML = '<p class="col-12 text-center text-muted">Cargando productos...</p>';
    }

    // --- Funciones para Renderizar HTML ---

    // Renderiza una sola tarjeta de producto
    function renderProductCard(producto) {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 col-lg-4 col-xl-3 mb-4';
        colDiv.innerHTML = `
            <div class="rounded position-relative fruite-item d-flex flex-column h-100">
                <a href="/shop-detail/${producto.id}/" class="text-decoration-none text-dark d-flex flex-column h-100">
                    <div class="fruite-img">
                        <img src="${producto.imagenUrl}" class="img-fluid w-100 rounded-top" alt="${producto.nombre}">
                    </div>
                    <div class="p-4 border border-warning border-top-0 rounded-bottom d-flex flex-column flex-grow-1">
                        <h4 class="mb-2">${producto.nombre}</h4>
                        <p class="text-muted mb-2">Marca: ${producto.marcaNombre || 'Desconocida'}</p>
                        <p class="text-muted mb-3">Categoría: ${producto.categoriaNombre || 'Desconocida'}</p>
                        
                        <p class="text-muted mb-3 product-description">
                            ${producto.descripcion || ''} 
                        </p>
                        
                        <div class="flex-grow-1"></div> <div class="d-flex justify-content-between align-items-center mt-auto">
                            <p class="text-dark fs-5 fw-bold mb-0">${formatPrice(producto.precio)}</p>
                                <a href="#" class="btn border border-secondary rounded-pill px-2 text-primary" style="white-space: nowrap;" onclick="event.stopPropagation(); alert('¡Producto ${producto.nombre} añadido al carrito!');">
                                    <i class="fa fa-shopping-bag me-1 text-primary"></i> Agregar
                                </a>
                        </div>
                    </div>
                </a>
            </div>
        `;
        shopProductsContainer.appendChild(colDiv);
    }

    // Renderiza la cuadrícula de productos
    function renderProducts(productos) {
        shopProductsContainer.innerHTML = ''; // Limpia el contenedor
        if (productos && productos.length > 0) {
            productos.forEach(producto => renderProductCard(producto));
        } else {
            shopProductsContainer.innerHTML = '<p class="col-12 text-center text-muted">No se encontraron productos con los filtros seleccionados.</p>';
        }
    }

    // Renderiza los controles de paginación
    function renderPagination(totalPages) {
        paginationControls.innerHTML = ''; // Limpia los controles existentes

        if (totalPages <= 1) return; // No mostrar paginación si solo hay una página

        // Botón "Anterior"
        const prevClass = currentFilters.page === 0 ? 'disabled' : '';
        paginationControls.innerHTML += `<a href="#" class="prev rounded ${prevClass}" data-page="${currentFilters.page - 1}">&laquo;</a>`;

        // Botones de número de página (mostrar un rango alrededor de la página actual)
        const startPage = Math.max(0, currentFilters.page - 2);
        const endPage = Math.min(totalPages - 1, currentFilters.page + 2);

        for (let i = startPage; i <= endPage; i++) {
            const activeClass = i === currentFilters.page ? 'active' : '';
            paginationControls.innerHTML += `<a href="#" class="rounded ${activeClass}" data-page="${i}">${i + 1}</a>`;
        }

        // Botón "Siguiente"
        const nextClass = currentFilters.page === totalPages - 1 ? 'disabled' : '';
        paginationControls.innerHTML += `<a href="#" class="next rounded ${nextClass}" data-page="${currentFilters.page + 1}">&raquo;</a>`;

        // Añadir event listeners a los botones de paginación recién creados
        paginationControls.querySelectorAll('a').forEach(button => {
            if (!button.classList.contains('disabled')) {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const newPage = parseInt(this.dataset.page);
                    if (!isNaN(newPage)) {
                        currentFilters.page = newPage;
                        fetchProducts(); // Vuelve a cargar productos con la nueva página
                    }
                });
            }
        });
    }

    // --- Funciones para cargar filtros dinámicamente ---

    // Carga y renderiza las categorías en la barra lateral
    function loadCategories() {
        fetch(`${apiBaseUrl}/categorias`) // Endpoint para obtener todas las categorías
            .then(response => {
                if (!response.ok) throw new Error('Error al cargar categorías');
                return response.json();
            })
            .then(categories => {
                // Limpiar y añadir la opción "Todas las categorías"
                categoryFilterList.innerHTML = `<li><a href="#" class="category-filter-item active-filter" data-category-name=""><i class="fas fa-arrow-alt-circle-right me-2"></i>Todas las categorías</a></li>`;
                categories.forEach(cat => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<a href="#" class="category-filter-item" data-category-name="${cat.nombre}"><i class="fas fa-arrow-alt-circle-right me-2"></i>${cat.nombre}</a>`;
                    categoryFilterList.appendChild(listItem);
                });
                addCategoryFilterListeners(); // Añadir listeners después de cargar
            })
            .catch(error => console.error('Error al cargar categorías:', error));
    }

    // Carga y renderiza las marcas en la barra lateral
    function loadBrands() {
        fetch(`${apiBaseUrl}/marcas`) // Endpoint para obtener todas las marcas
            .then(response => {
                if (!response.ok) throw new Error('Error al cargar marcas');
                return response.json();
            })
            .then(brands => {
                // Limpiar y añadir la opción "Todas las marcas"
                brandFilterList.innerHTML = `<li><a href="#" class="brand-filter-item active-filter" data-brand-name=""><i class="fas fa-arrow-alt-circle-right me-2"></i>Todas las marcas</a></li>`;
                brands.forEach(brand => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<a href="#" class="brand-filter-item" data-brand-name="${brand.nombre}"><i class="fas fa-arrow-alt-circle-right me-2"></i>${brand.nombre}</a>`;
                    brandFilterList.appendChild(listItem);
                });
                addBrandFilterListeners(); // Añadir listeners después de cargar
            })
            .catch(error => console.error('Error al cargar marcas:', error));
    }

    // --- Función Principal para Obtener Productos ---

    // Construye la URL de la API con los filtros y paginación actuales
    function buildApiUrl() {
        let url = new URL(`${apiBaseUrl}/productos/filter`); // Usamos el nuevo endpoint /productos/filter
        
        // Parámetros de paginación
        url.searchParams.append('page', currentFilters.page);
        url.searchParams.append('size', currentFilters.size);

        // Parámetros de búsqueda y filtrado
        if (currentFilters.search) {
            url.searchParams.append('search', currentFilters.search);
        }
        if (currentFilters.categoryName) {
            url.searchParams.append('categoriaNombre', currentFilters.categoryName);
        }
        if (currentFilters.brandName) {
            url.searchParams.append('marcaNombre', currentFilters.brandName);
        }
        if (currentFilters.minPrecio !== undefined && currentFilters.minPrecio !== null && currentFilters.minPrecio >= 0) {
            url.searchParams.append('minPrecio', currentFilters.minPrecio);
        }
        if (currentFilters.maxPrecio !== undefined && currentFilters.maxPrecio !== null && currentFilters.maxPrecio > 0) {
            url.searchParams.append('maxPrecio', currentFilters.maxPrecio);
        }
        if (currentFilters.sortBy) {
            url.searchParams.append('sort', currentFilters.sortBy);
        }
        return url.toString();
    }

    // Obtiene productos de la API con los filtros actuales
    function fetchProducts() {
        showLoading(); // Mostrar mensaje de carga
        const url = buildApiUrl();
        console.log("Fetching products from:", url); // Para depuración

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error de red o API: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                // La API ahora devuelve un objeto Page, donde 'content' es la lista de productos
                renderProducts(data.content);
                renderPagination(data.totalPages);

                // Desplazarse suavemente al inicio de la sección de productos
                const productsContainer = document.querySelector('.fruite.py-5'); // El contenedor principal de la tienda
                if (productsContainer) {
                    productsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            })
            .catch(error => {
                console.error('Error al obtener los productos:', error);
                shopProductsContainer.innerHTML = '<p class="col-12 text-danger text-center">No se pudieron cargar los productos en este momento. Intente de nuevo más tarde.</p>';
                paginationControls.innerHTML = ''; // Limpiar paginación si hay error
            });
    }

    // --- Event Listeners para Filtros y Paginación ---

    // Búsqueda por palabra clave
    searchButton.addEventListener('click', function() {
        currentFilters.search = searchKeywordsInput.value.trim();
        currentFilters.page = 0; // Resetear paginación al aplicar nuevo filtro
        fetchProducts();
    });
    searchKeywordsInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            searchButton.click();
        }
    });

    // Filtro de precios
    applyPriceFilterButton.addEventListener('click', function() {
        currentFilters.minPrecio = parseFloat(minPriceInput.value) || 0;
        currentFilters.maxPrecio = parseFloat(maxPriceInput.value) || 9999999;
        currentFilters.page = 0; // Resetear paginación
        fetchProducts();
    });

    // Dropdown de ordenación
    sortingDropdown.addEventListener('change', function() {
        currentFilters.sortBy = this.value;
        currentFilters.page = 0; // Resetear paginación
        fetchProducts();
    });

    // Event listeners para filtros de categoría (delegación de eventos)
    function addCategoryFilterListeners() {
        categoryFilterList.querySelectorAll('.category-filter-item').forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault();
                currentFilters.categoryName = this.dataset.categoryName; // Obtiene el nombre de la categoría
                currentFilters.page = 0; // Resetear paginación
                
                // Actualizar clase 'active-filter'
                categoryFilterList.querySelectorAll('.category-filter-item').forEach(li => li.classList.remove('active-filter'));
                this.classList.add('active-filter');

                fetchProducts();
            });
        });
    }

    // Event listeners para filtros de marca (delegación de eventos)
    function addBrandFilterListeners() {
        brandFilterList.querySelectorAll('.brand-filter-item').forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault();
                currentFilters.brandName = this.dataset.brandName; // Obtiene el nombre de la marca
                currentFilters.page = 0; // Resetear paginación

                // Actualizar clase 'active-filter'
                brandFilterList.querySelectorAll('.brand-filter-item').forEach(li => li.classList.remove('active-filter'));
                this.classList.add('active-filter');

                fetchProducts();
            });
        });
    }

    // --- Inicialización al cargar la página ---
    loadCategories(); // Cargar categorías para la barra lateral
    loadBrands();     // Cargar marcas para la barra lateral
    fetchProducts();  // Cargar productos iniciales

    // Añadir estilos básicos para los filtros activos y paginación (puedes mover esto a un archivo CSS)
    const style = document.createElement('style');
    style.innerHTML = `
        .fruite-categoriy .active-filter {
            font-weight: bold;
            color: #81C408; /* Color primario de tu plantilla */
            background-color: #e9ecef; /* Un gris claro para el fondo */
            border-radius: .375rem;
            padding: .25rem .5rem;
        }
        .pagination a.active {
            background-color: #81C408; /* Color primario de tu plantilla */
            color: white;
            border-color: #81C408;
        }
        .pagination a.disabled {
            pointer-events: none;
            opacity: 0.5;
        }
        .pagination a {
            display: inline-block;
            padding: 8px 16px;
            margin: 0 4px;
            color: #000;
            text-decoration: none;
            border: 1px solid #ddd;
            border-radius: 5px;
            transition: background-color .3s;
        }
        .pagination a:hover:not(.active):not(.disabled) {
            background-color: #ddd;
        }
    `;
    document.head.appendChild(style);
});