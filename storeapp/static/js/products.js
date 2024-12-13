window.onload = function() {
    let buttons = document.getElementsByClassName('add-to-cart');
    for(let btn of buttons)
    {
        btn.onclick = function(){
            let product_ids = localStorage.getItem('cart'); // Get cart from local storage
            if(product_ids){
                let cart_array = product_ids.split(','); // Convert string to array
                if(cart_array.includes(this.dataset['id'])){ // Check if product is already in cart
                    alert('Product is already in cart!'); // Alert user
                }
                else{ // If product is not in cart, add it
                    cart_array.push(this.dataset['id']); // Add product to cart
                    localStorage.setItem('cart', cart_array); // Update cart
                }
            }
            else{
                localStorage.setItem('cart', this.dataset['id']); // Add product to cart
            }
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filter_form');
    var priceRange = document.querySelector('input[name="price_range"]');
    var priceValue = document.getElementById('price_value');
    if (priceRange) {
        priceValue.textContent = priceRange.value;
        priceRange.addEventListener('input', function() {
            priceValue.textContent = priceRange.value;
        });
    }

    var priceRangeField = document.getElementById('id_price_range');
    if (priceRangeField) {
        priceRangeField.oninput = function() {
            document.getElementById('price_value').innerText = this.value;
        };
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent traditional form submission
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
            productsList.innerHTML = `
            <div class="col-md-9">
                    <div id="products_list" class="card">
                        <div class="card-header">
                            <h1>Products</h1>
                        </div>
                    <div class="row">`;
            if (data.products && data.products.length > 0) {
                data.products.forEach(product => {
                    let productItem = document.createElement('div');
                    productItem.className = 'col-12';
                    productItem.innerHTML = `
                        <a href="/storeapp/product/${product.product_id}">
                            <div class="card mb-4 shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title">${product.name}</h5>
                                    <p class="card-text">${product.price}</p>
                                    <p class="card-text">${product.product_id}</p>
                                </div>
                            </div>
                        </a>
                    `;
                    productsList.appendChild(productItem);
                });
                let ending = `</div></div></div>`;
                productsList.appendChild(ending);
            } else {
                productsList.innerHTML = '<p>No products found.</p>';
            }

            // Pagination
            let pagination = document.querySelector('.pagination');
            pagination.innerHTML = '';
            if (data.pagination) {
                if (data.pagination.has_previous) {
                    let prevItem = document.createElement('li');
                    prevItem.className = 'page-item';
                    prevItem.innerHTML = `<a class="page-link" href="?page=${data.pagination.current_page - 1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>`;
                    pagination.appendChild(prevItem);
                }
                for (let i = 1; i <= data.pagination.num_pages; i++) {
                    let pageItem = document.createElement('li');
                    pageItem.className = `page-item ${i === data.pagination.current_page ? 'active' : ''}`;
                    pageItem.innerHTML = `<a class="page-link" href="?page=${i}">${i}</a>`;
                    pagination.appendChild(pageItem);
                }
                if (data.pagination.has_next) {
                    let nextItem = document.createElement('li');
                    nextItem.className = 'page-item';
                    nextItem.innerHTML = `<a class="page-link" href="?page=${data.pagination.current_page + 1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>`;
                    pagination.appendChild(nextItem);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
});