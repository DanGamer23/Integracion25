// web/static/js/shop_products.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Referencias a elementos del DOM (Globales / Carrito - Deben existir en base.html) ---
    const cartCounter = document.getElementById('cart-counter');
    const cartItemsContainer = document.getElementById('cart-items-container');
    const cartEmptyMessage = document.getElementById('cart-empty-message');
    const cartTotalElement = document.getElementById('cart-total');
    const checkoutButton = document.getElementById('checkout-button');
    const shoppingCartModalElement = document.getElementById('shoppingCartModal');
    const shoppingCartModal = new bootstrap.Modal(shoppingCartModalElement); // Inicializa el objeto modal

    // ** IMPORTANTE: URL base de tu API de Spring Boot **
    const apiBaseUrl = 'http://localhost:8080';

    // --- Estado del Carrito ---
    const CART_STORAGE_KEY = 'shoppingCart';
    let cart = []; // Array para almacenar los productos en el carrito

    // --- Funciones de Utilidad (Globales) ---

    function formatPrice(price) {
        return new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP',
            minimumFractionDigits: 0
        }).format(price);
    }

    // Función para mostrar Toasts (NOTIFICACIONES)
    function showToast(message, type = 'success') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            console.error('Toast container not found! Falling back to alert.');
            alert(message); // Fallback si no se encuentra el contenedor del toast
            return;
        }

        const toastDiv = document.createElement('div');
        toastDiv.className = `toast align-items-center text-white bg-${type} border-0`;
        toastDiv.setAttribute('role', 'alert');
        toastDiv.setAttribute('aria-live', 'assertive');
        toastDiv.setAttribute('aria-atomic', 'true');
        toastDiv.setAttribute('data-bs-delay', '3000'); // Duración de 3 segundos

        toastDiv.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        toastContainer.appendChild(toastDiv);
        const bsToast = new bootstrap.Toast(toastDiv);
        bsToast.show();

        // Limpiar el elemento toast después de que se oculte para no llenar el DOM
        toastDiv.addEventListener('hidden.bs.toast', function () {
            toastDiv.remove();
        });
    }

    // showLoading - Universal para cualquier carga de productos
    function showLoading(container) {
        if (container) {
            container.innerHTML = '<p class="col-12 text-center text-muted">Cargando productos...</p>';
        }
    }


    // --- Funciones del Carrito (Globales) ---

    function loadCart() {
        const storedCart = sessionStorage.getItem(CART_STORAGE_KEY);
        if (storedCart) {
            try {
                cart = JSON.parse(storedCart);
            } catch (e) {
                console.error("Error parsing cart from sessionStorage:", e);
                cart = [];
                showToast('Error al cargar el carrito guardado. Se ha reiniciado.', 'danger');
            }
        } else {
            cart = [];
        }
        updateCartCounter();
    }

    function saveCart() {
        sessionStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    }

    // Modificada para aceptar una cantidad
    async function addToCart(product, quantity = 1) {
        const existingItem = cart.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += quantity;
            showToast(`Cantidad de "${product.nombre}" actualizada a ${existingItem.quantity}.`, 'info');
        } else {
            cart.push({
                id: product.id,
                nombre: product.nombre,
                precio: product.precio,
                imagenUrl: product.imagenUrl,
                quantity: quantity
            });
            showToast(`"${product.nombre}" (${quantity} unidades) añadido al carrito.`, 'success');
        }
        saveCart();
        updateCartCounter();
        if (shoppingCartModalElement.classList.contains('show')) {
             renderCartModalContent();
        }
    }

    function updateCartItemQuantity(productId, change) {
        const itemIndex = cart.findIndex(item => item.id === productId);
        if (itemIndex > -1) {
            cart[itemIndex].quantity += change;
            if (cart[itemIndex].quantity <= 0) {
                removeItemFromCart(productId);
                showToast(`"${cart[itemIndex]?.nombre || 'Producto'}" eliminado del carrito.`, 'danger');
                return;
            }
            saveCart();
            updateCartCounter();
            renderCartModalContent();
        }
    }

    function removeItemFromCart(productId) {
        const itemToRemove = cart.find(item => item.id === productId);
        cart = cart.filter(item => item.id !== productId);
        saveCart();
        updateCartCounter();
        renderCartModalContent();
        if (itemToRemove) {
             showToast(`"${itemToRemove.nombre}" eliminado del carrito.`, 'danger');
        }
    }

    function renderCartModalContent() {
        cartItemsContainer.innerHTML = '';
        if (cart.length === 0) {
            cartEmptyMessage.style.display = 'block';
            cartTotalElement.textContent = formatPrice(0);
            checkoutButton.disabled = true;
        } else {
            cartEmptyMessage.style.display = 'none';
            checkoutButton.disabled = false;

            let total = 0;
            cart.forEach(item => {
                const itemSubtotal = item.precio * item.quantity;
                total += itemSubtotal;

                const cartItemDiv = document.createElement('div');
                cartItemDiv.className = 'list-group-item d-flex align-items-center mb-2 p-3 border rounded';
                cartItemDiv.innerHTML = `
                    <img src="${item.imagenUrl}" alt="${item.nombre}" style="width: 70px; height: 70px; object-fit: contain; margin-right: 15px; border-radius: 5px;">
                    <div class="flex-grow-1">
                        <h6 class="mb-0">${item.nombre}</h6>
                        <small class="text-muted">${formatPrice(item.precio)} c/u</small>
                    </div>
                    <div class="d-flex align-items-center me-3">
                        <button class="btn btn-sm btn-outline-secondary cart-qty-minus" data-id="${item.id}">-</button>
                        <span class="px-2 fw-bold">${item.quantity}</span>
                        <button class="btn btn-sm btn-outline-secondary cart-qty-plus" data-id="${item.id}">+</button>
                    </div>
                    <div class="text-end me-3">
                        <h6 class="mb-0 fw-bold">${formatPrice(itemSubtotal)}</h6>
                    </div>
                    <button class="btn btn-sm btn-danger ms-2 cart-remove-item" data-id="${item.id}" title="Eliminar">
                        <i class="fa fa-trash"></i>
                    </button>
                `;
                cartItemsContainer.appendChild(cartItemDiv);
            });
            cartTotalElement.textContent = formatPrice(total);
        }
        updateCartCounter();
    }

    function updateCartCounter() {
        const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCounter.textContent = itemCount;
        checkoutButton.disabled = cart.length === 0;
    }

    // --- Referencias Específicas de la Página de Tienda o Índice ---
    const shopProductsContainer = document.getElementById('shop-products-container'); // Contenedor para la página de tienda
    const homeProductsContainer = document.getElementById('productos-container'); // Contenedor para la página de índice

    // DECLARACIONES DE VARIABLES PARA LA PÁGINA DE DETALLE (inicializadas a null)
    let productDetailQtyInput = null;
    let qtyMinusBtn = null;
    let qtyPlusBtn = null;
    let addToCartDetailBtn = null;
    let relatedProductsContainer = null;


    const categoryFilterList = document.getElementById('category-filter-list');
    const brandFilterList = document.getElementById('brand-filter-list');
    const searchKeywordsInput = document.getElementById('search-keywords');
    const searchButton = document.getElementById('search-button');
    const minPriceInput = document.getElementById('min-price');
    const maxPriceInput = document.getElementById('max-price');
    const applyPriceFilterButton = document.getElementById('apply-price-filter');
    const sortingDropdown = document.getElementById('sorting-dropdown');
    const paginationControls = document.getElementById('pagination-controls');
    // currentFilters solo es relevante para la página de tienda
    let currentFilters = {
        search: '',
        categoryName: '',
        brandName: '',
        minPrecio: 0,
        maxPrecio: 9999999,
        sortBy: '',
        page: 0,
        size: 8
    };
    // Renderiza una sola tarjeta de producto (USADA POR AMBOS CONTENEDORES)
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
                        
                        <div class="flex-grow-1"></div>

                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <p class="text-dark fs-5 fw-bold mb-0">${formatPrice(producto.precio)}</p>
                            <button class="btn border border-secondary rounded-pill px-2 text-primary add-to-cart-btn" data-product-id="${producto.id}" type="button">
                                <i class="fa fa-shopping-bag me-1 text-primary"></i> Agregar
                            </button>
                        </div>
                    </div>
                </a>
            </div>
        `;
        return colDiv;
    }

    // Renderiza productos en un contenedor dado
    function renderProductsInContainer(productos, container) {
        if (container) {
            container.innerHTML = '';
            if (productos && productos.length > 0) {
                productos.forEach(producto => {
                    const productCard = renderProductCard(producto);
                    container.appendChild(productCard);
                });
            } else {
                container.innerHTML = '<p class="col-12 text-center text-muted">No se encontraron productos.</p>';
            }
        }
    }

    // Funciones de filtro y paginación (Solo para la página de tienda)
    function buildApiUrl() {
        const params = new URLSearchParams();
        if (currentFilters.search) params.append('search', currentFilters.search);
        if (currentFilters.categoryName) params.append('categoriaNombre', currentFilters.categoryName);
        if (currentFilters.brandName) params.append('marcaNombre', currentFilters.brandName);
        params.append('minPrecio', currentFilters.minPrecio);
        params.append('maxPrecio', currentFilters.maxPrecio);
        if (currentFilters.sortBy) params.append('sortBy', currentFilters.sortBy);
        params.append('page', currentFilters.page);
        params.append('size', currentFilters.size);
        return `${apiBaseUrl}/productos/filter?${params.toString()}`;
    }

    function fetchShopProducts() {
        if (!shopProductsContainer) return;
        showLoading(shopProductsContainer); // Pasa el contenedor a showLoading
        const url = buildApiUrl();
        console.log("Fetching products for shop from:", url);

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error de red o API: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                renderProductsInContainer(data.content, shopProductsContainer);
                renderPagination(data.totalPages);

                const productsSection = document.querySelector('.fruite.py-5');
                if (productsSection) {
                    productsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            })
            .catch(error => {
                console.error('Error al obtener los productos de la tienda:', error);
                shopProductsContainer.innerHTML = '<p class="col-12 text-danger text-center">No se pudieron cargar los productos en este momento. Intente de nuevo más tarde.</p>';
                if (paginationControls) {
                    paginationControls.innerHTML = '';
                }
                showToast('Error al cargar productos de la tienda. Intente más tarde.', 'danger');
            });
    }

    // Función para cargar productos para la página de índice
    function fetchHomeProducts() {
        if (!homeProductsContainer) return;
        showLoading(homeProductsContainer); // Pasa el contenedor a showLoading
        const url = `${apiBaseUrl}/productos`;
        // O la URL de tu API para obtener todos los productos
        console.log("Fetching products for home page from:", url);
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error de red o API: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(productos => {
                // Tomar solo los primeros 8 productos para la página de inicio
                const productsToShow = productos.slice(0, 8);
                renderProductsInContainer(productsToShow, homeProductsContainer);
            })
            .catch(error => {
                console.error('Error al obtener los productos para la página de inicio:', error);
                homeProductsContainer.innerHTML = '<p class="col-12 text-danger text-center">No se pudieron cargar los productos destacados en este momento.</p>';
                showToast('Error al cargar productos destacados. Intente más tarde.', 'danger');
            });
    }

    // Lógica para cargar productos relacionados (opcional)
    async function fetchRelatedProducts(currentProductId, categoryName, brandName) {
        if (!relatedProductsContainer) return;
        relatedProductsContainer.innerHTML = '<p class="text-center text-muted">Cargando productos relacionados...</p>';

        const params = new URLSearchParams();
        if (categoryName) params.append('categoryName', categoryName);
        if (brandName) params.append('brandName', brandName);
        params.append('size', 4); // Cargar solo 4 productos relacionados
        params.append('page', 0);
        params.append('excludeId', currentProductId); // AÑADIDO PARA EXCLUIR EL PRODUCTO ACTUAL

        const url = `${apiBaseUrl}/productos/filter?${params.toString()}`;
        console.log("Fetching related products from:", url);

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Error al cargar relacionados: ${response.status} ${response.statusText}`);
            }
            const data = await response.json();
            
            if (data.content && data.content.length > 0) {
                relatedProductsContainer.innerHTML = '';
                data.content.forEach(producto => {
                    const relatedProductDiv = document.createElement('div');
                    relatedProductDiv.className = 'd-flex align-items-center mb-4';
                    relatedProductDiv.innerHTML = `
                        <div class="rounded" style="width: 100px; height: 100px; overflow: hidden; display: flex; justify-content: center; align-items: center; border: 1px solid #eee;">
                            <img src="${producto.imagenUrl}" class="img-fluid rounded" alt="${producto.nombre}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                        </div>
                        <div class="ms-3">
                            <a href="/shop-detail/${producto.id}/" class="h5 d-inline-block text-decoration-none text-dark">${producto.nombre}</a>
                            <p class="text-dark mb-0">${formatPrice(producto.precio)}</p>
                        </div>
                    `;
                    relatedProductsContainer.appendChild(relatedProductDiv);
                });
            } else {
                relatedProductsContainer.innerHTML = '<p class="text-muted">No se encontraron productos relacionados.</p>';
            }

        } catch (error) {
            console.error('Error al obtener productos relacionados:', error);
            relatedProductsContainer.innerHTML = '<p class="text-danger">Error al cargar productos relacionados.</p>';
            showToast('Error al cargar productos relacionados. Intente más tarde.', 'danger');
        }
    }


    // Listeners para los filtros y paginación (Solo para la página de tienda)
function addCategoryFilterListeners() {
    document.querySelectorAll('.category-filter-item').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            document.querySelectorAll('.category-filter-item').forEach(el => el.classList.remove('active-filter'));
            this.classList.add('active-filter');

            currentFilters.categoryName = this.dataset.categoryName || '';
            currentFilters.page = 0;
            fetchShopProducts();
        });
    });
}

function addBrandFilterListeners() {
    document.querySelectorAll('.brand-filter-item').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            document.querySelectorAll('.brand-filter-item').forEach(el => el.classList.remove('active-filter'));
            this.classList.add('active-filter');

            currentFilters.brandName = this.dataset.brandName || '';
            currentFilters.page = 0;
            fetchShopProducts();
        });
    });
}

function loadCategories() {
    if (!categoryFilterList) return;

    fetch(`${apiBaseUrl}/categorias`)
        .then(response => response.json())
        .then(categories => {
            categoryFilterList.innerHTML = `
                <li>
                    <a href="#" class="category-filter-item active-filter" data-category-name="">
                        <i class="fas fa-arrow-alt-circle-right me-2"></i>Todas las categorías
                    </a>
                </li>`;

            categories.forEach(cat => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <a href="#" class="category-filter-item" data-category-name="${cat.nombre}">
                        <i class="fas fa-arrow-alt-circle-right me-2"></i>${cat.nombre}
                    </a>`;
                categoryFilterList.appendChild(li);
            });

            addCategoryFilterListeners();
        })
        .catch(error => {
            console.error('Error al cargar categorías:', error);
            showToast('Error al cargar categorías.', 'danger');
        });
}

function loadBrands() {
    if (!brandFilterList) return;

    fetch(`${apiBaseUrl}/marcas`)
        .then(response => response.json())
        .then(brands => {
            brandFilterList.innerHTML = `
                <li>
                    <a href="#" class="brand-filter-item active-filter" data-brand-name="">
                        <i class="fas fa-arrow-alt-circle-right me-2"></i>Todas las marcas
                    </a>
                </li>`;

            brands.forEach(brand => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <a href="#" class="brand-filter-item" data-brand-name="${brand.nombre}">
                        <i class="fas fa-arrow-alt-circle-right me-2"></i>${brand.nombre}
                    </a>`;
                brandFilterList.appendChild(li);
            });

            addBrandFilterListeners();
        })
        .catch(error => {
            console.error('Error al cargar marcas:', error);
            showToast('Error al cargar marcas.', 'danger');
        });
}

    function renderPagination(totalPages) {
        if (!paginationControls) return;
        paginationControls.innerHTML = '';
        if (totalPages <= 1) return;

        const createPaginationLink = (page, text, isDisabled = false, isActive = false) => {
            const li = document.createElement('li');
            li.className = `page-item ${isDisabled ? 'disabled' : ''} ${isActive ? 'active' : ''}`;
            const a = document.createElement('a');
            a.className = `page-link ${isDisabled ? 'disabled' : ''} ${isActive ? 'active' : ''}`;
            a.href = '#';
            a.dataset.page = page;
            a.innerHTML = text;
            li.appendChild(a);
            return li;
        };

        paginationControls.appendChild(
            createPaginationLink(currentFilters.page - 1, '&laquo;', currentFilters.page === 0)
        );
        let startPage = Math.max(0, currentFilters.page - 2);
        let endPage = Math.min(totalPages - 1, currentFilters.page + 2);
        if (currentFilters.page < 2) {
            endPage = Math.min(totalPages - 1, 4);
        }
        if (currentFilters.page > totalPages - 3) {
            startPage = Math.max(0, totalPages - 5);
        }

        if (startPage > 0) {
            paginationControls.appendChild(createPaginationLink(0, '1'));
            if (startPage > 1) {
                const ellipsis = document.createElement('li');
                ellipsis.className = 'page-item disabled';
                ellipsis.innerHTML = '<span class="page-link">...</span>';
                paginationControls.appendChild(ellipsis);
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            paginationControls.appendChild(
                createPaginationLink(i, i + 1, false, i === currentFilters.page)
            );
        }

        if (endPage < totalPages - 1) {
            if (endPage < totalPages - 2) {
                const ellipsis = document.createElement('li');
                ellipsis.className = 'page-item disabled';
                ellipsis.innerHTML = '<span class="page-link">...</span>';
                paginationControls.appendChild(ellipsis);
            }
            paginationControls.appendChild(createPaginationLink(totalPages - 1, totalPages));
        }

        paginationControls.appendChild(
            createPaginationLink(currentFilters.page + 1, '&raquo;', currentFilters.page === totalPages - 1)
        );
    }

    function addShopPageListeners() {
        if (searchButton) {
            searchButton.addEventListener('click', function() {
                currentFilters.search = searchKeywordsInput.value;
                currentFilters.page = 0;
                fetchShopProducts();
            });
        }
        if (searchKeywordsInput) {
            searchKeywordsInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    searchButton.click();
                }
            });
        }
        if (applyPriceFilterButton) {
            applyPriceFilterButton.addEventListener('click', function() {
                currentFilters.minPrecio = parseFloat(minPriceInput.value) || 0;
                currentFilters.maxPrecio = parseFloat(maxPriceInput.value) || 9999999;
                currentFilters.page = 0;
                fetchShopProducts();
            });
        }
        
        if (sortingDropdown) {
            sortingDropdown.addEventListener('change', function() {
                currentFilters.sortBy = this.value;
                currentFilters.page = 0;
                fetchShopProducts();
            });
        }

        if (paginationControls) {
            paginationControls.addEventListener('click', function(event) {
                const target = event.target;
                if (target.tagName === 'A' && !target.classList.contains('disabled')) {
                    event.preventDefault();
                    const newPage = parseInt(target.dataset.page);
                    if (!isNaN(newPage)) {
                        currentFilters.page = newPage;
                        fetchShopProducts();
                    }
                }
            });
        }
    }


    // --- GLOBAL Event Listeners para el Carrito ---

    // Delegación de eventos para los botones de "Agregar al Carrito" en cualquier parte del documento
    // Ahora maneja el botón de detalle de producto directamente
    document.body.addEventListener('click', async function(event) {
        const target = event.target;
        // Busca el botón más cercano con la clase 'add-to-cart-btn'
        const button = target.closest('.add-to-cart-btn');

        if (button) {
            event.preventDefault();
            event.stopPropagation(); // Aquí también agregamos stopPropagation

            const productId = parseInt(button.dataset.productId);
            let quantity = 1;

            // Si es el botón de la página de detalle de producto, obtener la cantidad del input
            // MODIFICADO: usamos la referencia productDetailQtyInput que se inicializará en el if de detalle
            if (button.id === 'add-to-cart-detail-btn' && productDetailQtyInput) {
                quantity = parseInt(productDetailQtyInput.value) || 1;
                if (quantity < 1) quantity = 1; // Asegurar que la cantidad sea al menos 1
            }

            try {
                const response = await fetch(`${apiBaseUrl}/productos/${productId}`);
                if (!response.ok) {
                    throw new Error('Producto no encontrado en la API.');
                }
                const productDetails = await response.json();
                await addToCart(productDetails, quantity); // Pasa la cantidad
            } catch (error) {
                console.error('Error al obtener detalles del producto para el carrito:', error);
                showToast('No se pudo añadir el producto al carrito. Intente de nuevo.', 'danger');
            }
        }
    });


    // Delegación de eventos para los botones de cantidad (+/-) y eliminar dentro del MODAL del carrito
    // ESTE BLOQUE ES CORRECTO Y DEBE PERMANECER (ya no contiene los botones de detalle)
    document.body.addEventListener('click', function(event) {
        const target = event.target;
        const button = target.closest('.cart-qty-plus, .cart-qty-minus, .cart-remove-item'); // Solo botones del modal

        if (button) {
            const productId = parseInt(button.dataset.id); // productId se obtiene del data-id del botón en el modal
            if (isNaN(productId)) return;

            if (button.classList.contains('cart-qty-plus')) {
                updateCartItemQuantity(productId, 1);
            } else if (button.classList.contains('cart-qty-minus')) {
                updateCartItemQuantity(productId, -1);
            } else if (button.classList.contains('cart-remove-item')) {
                removeItemFromCart(productId);
            }
        }
    });

    // Evento para cuando se abre el modal del carrito
    shoppingCartModalElement.addEventListener('show.bs.modal', renderCartModalContent);

    // --- Inicialización al cargar la página ---
    loadCart(); // SIEMPRE cargar el carrito desde sessionStorage al inicio de CUALQUIER página

    // Lógica para la página de TIENDA: si existen los elementos de filtro/paginación
    if (shopProductsContainer && categoryFilterList && brandFilterList && searchButton && sortingDropdown && paginationControls && minPriceInput && maxPriceInput && applyPriceFilterButton) {
        console.log("Inicializando lógica específica de la página de tienda...");
        loadCategories();
        loadBrands();
        fetchShopProducts();
        addShopPageListeners();
    }
    // Lógica para la página de INICIO (Index): si solo existe el contenedor de productos destacados
    else if (homeProductsContainer) {
        console.log("Inicializando lógica para la página de inicio (productos destacados)...");
        fetchHomeProducts();
    }

    // Lógica para la página de DETALLE DE PRODUCTO: si existe el input de cantidad y el botón de agregar
    else if (document.getElementById('product-qty-input') && document.getElementById('add-to-cart-detail-btn')) {
        console.log("Inicializando lógica para la página de detalle de producto...");

        productDetailQtyInput = document.getElementById('product-qty-input');
        qtyMinusBtn = document.getElementById('qty-minus-btn');
        qtyPlusBtn = document.getElementById('qty-plus-btn');
        addToCartDetailBtn = document.getElementById('add-to-cart-detail-btn');
        relatedProductsContainer = document.getElementById('related-products-container');


        if (productDetailQtyInput) {
            productDetailQtyInput.value = '1'; // Establece el valor inicial a 1 como cadena
        }

        const currentProductId = parseInt(addToCartDetailBtn.dataset.productId);
        const currentProductCategory = addToCartDetailBtn.dataset.categoryName;
        const currentProductBrand = addToCartDetailBtn.dataset.brandName;
        
        if (relatedProductsContainer) {
            fetchRelatedProducts(currentProductId, currentProductCategory, currentProductBrand);
        }

        if (qtyMinusBtn && productDetailQtyInput) {
            qtyMinusBtn.addEventListener('click', function() {
                let currentQty = Number(productDetailQtyInput.value.trim()); // Usar Number()
                if (typeof currentQty !== 'number' || isNaN(currentQty)) {
                    currentQty = 1; 
                }
                console.log('Minus clicked: currentQty before:', currentQty);
                if (currentQty > 1) {
                    productDetailQtyInput.value = (currentQty - 1).toString(); // Convertir explícitamente a cadena
                } else {
                    productDetailQtyInput.value = '1'; // Asegurarse de que no baje de 1
                }
                console.log('Minus clicked: currentQty after:', productDetailQtyInput.value);
            });
        }

        if (qtyPlusBtn && productDetailQtyInput) {
            qtyPlusBtn.addEventListener('click', function() {
                let currentQty = Number(productDetailQtyInput.value.trim()); // Usar Number()
                if (typeof currentQty !== 'number' || isNaN(currentQty)) {
                    currentQty = 0; // Si por alguna razón es NaN, establecer a 0
                }
                console.log('Plus clicked: currentQty before:', currentQty);
                productDetailQtyInput.value = (currentQty + 1).toString(); // Convertir explícitamente a cadena
                console.log('Plus clicked: currentQty after:', productDetailQtyInput.value);
            });
        }
    }
    // Si no es ninguna de las anteriores, solo se carga la lógica del carrito.
    else {
        console.log("No es la página de tienda, ni de inicio, ni de detalle de producto completa. Solo se carga la lógica del carrito.");
    }

    checkoutButton.addEventListener('click', function () {
        if (!cart || cart.length === 0) {
            showToast('El carrito está vacío. Añade productos antes de proceder al pago.', 'warning');
            return;
        }

        fetch('http://127.0.0.1:8001/iniciar-pago/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ cart: cart })
        })
        .then(response => {
            console.log("Respuesta completa:", response);
            return response.json();
        })
        .then(data => {
            if (data.init_point) {
                window.location.href = data.init_point;
            } else {
                showToast('Error al iniciar el pago. Intenta de nuevo.', 'danger');
            }
        })
        .catch(error => {
            console.error('Error al procesar el pago:', error);
            showToast('No se pudo iniciar el pago. Revisa tu conexión.', 'danger');
        });
    });


    function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
    }


    // --- ESTILOS PARA LA UNIFORMIDAD DE LAS TARJETAS (VERSION AJUSTADA) ---
    const style = document.createElement('style');
    style.innerHTML = `
        /* Estilos existentes para filtros y paginación */
        .fruite-categoriy .active-filter {
            font-weight: bold;
            color: #81C408;
            background-color: #e9ecef;
            border-radius: .375rem;
            padding: .25rem .5rem;
        }
        .pagination a.active {
            background-color: #81C408;
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

        /* --- ESTILOS OPCIONALES PARA LA UNIFORMIDAD DE LAS TARJETAS --- */
        .fruite-img {
            height: 180px;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #fff;
            padding: 10px;
        }
        .fruite-img img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            object-position: center;
        }
        .product-description {
            line-height: 1.5em;
            height: 4.5em;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3; 
            -webkit-box-orient: vertical;
            word-break: break-word;
        }
        .fruite-item > a.d-flex {
            min-height: 100%;
        }

        /* ESTILO PARA EL BOTÓN AGREGAR - Asegura tamaño consistente y evita salto de línea */
        .add-to-cart-btn {
            white-space: nowrap;
            min-width: 100px;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        /* Ajustes visuales para los ítems del carrito en el modal */
        #cart-items-container .list-group-item img {
            border: 1px solid #eee;
        }
        #cart-items-container .list-group-item .btn-sm {
            padding: .25rem .5rem;
            font-size: .875rem;
            line-height: 1.5;
            border-radius: .2rem;
        }

        /* Asegura que el toast esté por encima de otros elementos como el modal */
        .toast-container {
            z-index: 1080;
        }

        /* Estilo específico para el input de cantidad en la página de detalle */
        #product-qty-input {
            width: 50px !important;
            /* Fuerza un ancho para el input de cantidad */
        }
    `;
    document.head.appendChild(style);
});