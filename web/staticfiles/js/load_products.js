document.addEventListener('DOMContentLoaded', function() {
 const productosContainer = document.getElementById('productos-container');
    const apiProductosUrl = 'http://127.0.0.1:8080/productos'; 

    // Función para formatear el precio como CLP (o tu moneda local)
    function formatPrice(price) {
        return new Intl.NumberFormat('es-CL', { 
            style: 'currency', 
            currency: 'CLP', 
            minimumFractionDigits: 0 
        }).format(price);
    }

    fetch(apiProductosUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error de red o API: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(productos => {
            const productosToShow = productos.slice(0, 8); 
            
            productosToShow.forEach(producto => {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-6 col-lg-4 col-xl-3 mb-4'; // Añadí mb-4 para un poco de margen inferior entre filas

                // Estructura HTML de la tarjeta de producto con clases Flexbox y CSS para consistencia
                colDiv.innerHTML = `
                    <div class="rounded position-relative fruite-item d-flex flex-column h-100">
                        <div class="fruite-img">
                            <img src="${producto.imagenUrl}" class="img-fluid w-100 rounded-top" alt="${producto.nombre}">
                        </div>
                        <div class="p-4 border border-warning border-top-0 rounded-bottom d-flex flex-column flex-grow-1">
                            <h4 class="mb-2">${producto.nombre}</h4>
                            
                            <p class="text-muted mb-3" style="min-height: 4.5em; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical;">
                                ${producto.descripcion || ''} 
                            </p>
                            
                            <div class="flex-grow-1"></div> 

                            <div class="d-flex justify-content-between flex-wrap mt-auto">
                                <p class="text-dark fs-5 fw-bold mb-0">${formatPrice(producto.precio)}</p>
                                <a href="#" class="btn border border-secondary rounded-pill px-3 text-primary">
                                    <i class="fa fa-shopping-bag me-2 text-primary"></i> Agregar al carrito
                                </a>
                            </div>
                        </div>
                    </div>
                `;
                productosContainer.appendChild(colDiv);
            });
        })
        .catch(error => {
            console.error('Error al obtener los productos:', error);
            productosContainer.innerHTML = '<p class="text-danger">No se pudieron cargar los productos en este momento. Intente de nuevo más tarde.</p>';
        });
});