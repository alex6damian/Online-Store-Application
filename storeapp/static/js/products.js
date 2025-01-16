document.addEventListener('DOMContentLoaded', function() {
    let filterButton = document.getElementById('filter-button');
    if (!filterButton) {
        console.error('Filter button not found');
        return;
    }
    filterButton.onclick = function(event) {
        event.preventDefault();
        
        const form = document.getElementById('filter_form');
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });
        fetch(`/storeapp/filter_products/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF token for security
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            let productsList = document.getElementById('products_list');
            productsList.innerHTML = '';
            productsList.className = 'card';
            if (data.products && data.products.length > 0) {
                data.products.forEach(product => {
                    let productItem = document.createElement('div');
                    productItem.className = 'card-body d-flex justify-content-between align-items-center';
                    productItem.innerHTML = `
                        <div>
                            <a href="/storeapp/product/${product.id}">
                                <h3 class="card-title">${product.name}</h3>
                            </a>
                            <p class="card-text">Price: $${product.price}</p>
                        </div>
                        <button class='add-to-cart btn btn-success' data-name='${product.name}' data-stock='${product.stock}' data-price='${product.price}' data-id='${product.product_id}'>Add to cart</button>
                    `;
                    productsList.appendChild(productItem);
                });
            } else {
                productsList.innerHTML = '<p>No products found.</p>';
            }

            // Pagination
            let paginationContainer = document.querySelector('.pagination');
            if (!paginationContainer) {
                console.error('Pagination container not found');
                return;
            }
            paginationContainer.innerHTML = `
                <nav aria-label="Page navigation">
                    <ul class="pagination justify-content-center"></ul>
                </nav>
            `;
            let pagination = paginationContainer.querySelector('ul');
            if (data.pagination) {
                if (data.pagination.has_previous) {
                    let prevItem = document.createElement('li');
                    prevItem.className = 'page-item';
                    prevItem.innerHTML = `<a class="page-link" href="?page=${data.pagination.previous_page_number}" aria-label="Previous"><span aria-hidden="true">previous</span></a>`;
                    pagination.appendChild(prevItem);
                }
                let pageInfoItem = document.createElement('li');
                pageInfoItem.className = 'page-item disabled';
                pageInfoItem.innerHTML = `<span class="page-link">Page ${data.pagination.current_page} of ${data.pagination.num_pages}.</span>`;
                pagination.appendChild(pageInfoItem);
                if (data.pagination.has_next) {
                    let nextItem = document.createElement('li');
                    nextItem.className = 'page-item';
                    nextItem.innerHTML = `<a class="page-link" href="?page=${data.pagination.next_page_number}" aria-label="Next"><span aria-hidden="true">next</span></a>`;
                    pagination.appendChild(nextItem);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
});