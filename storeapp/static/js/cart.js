document.addEventListener('DOMContentLoaded', function() {
    let cartData = localStorage.getItem('cart')
    const cartItemsContainer = document.getElementById('cart-items-container');
    const totalPriceElement = document.getElementById('total-price');
    let totalPrice = 0;

    if (cartData) {
        cartData = JSON.parse(cartData);
    } else {
        cartData = [];
    }
    cartItemsContainer.innerHTML = '';

    if (cartData.length === 0) {
        cartItemsContainer.innerHTML = 'Your cart is empty!';
    }

    cartData.forEach(item => {
        const { id, name, price, quantity, stock } = item;
        const itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');
        itemElement.innerHTML = `
            <div class="item-name" style="font-weight: bold; margin-top: 15px; margin-bottom: 1px;">Product name: ${name}</div>
            <div class="item-price" style="color: gray; font-weight: bold; margin-bottom: 1px;">Price: $${price}</div>
            <div class="item-quantity" style="margin-bottom: 5px;">Quantity: ${quantity}</div>
            `;
        const quantityControls = document.createElement('div');
        quantityControls.classList.add('quantity-controls');

        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.value = quantity;
        quantityInput.min = 0;
        quantityInput.max = stock;
        quantityInput.addEventListener('change', (event) => {
            const newQuantity = parseInt(event.target.value);
            if (newQuantity >= 0 && newQuantity <= stock) {
                item.quantity = newQuantity;
                localStorage.setItem('cart', JSON.stringify(cartData));
                location.reload();
            } else {
                alert('Not enough stock! Only ' + stock + ' left.');
                event.target.value = quantity;
            }
        });
        quantityControls.appendChild(quantityInput);

        const increaseButton = document.createElement('button');
        increaseButton.textContent = '+';
        increaseButton.addEventListener('click', () => {
            if (item.quantity < stock) {
            item.quantity++;
            localStorage.setItem('cart', JSON.stringify(cartData));
            location.reload();
        }
            else {
                alert('Not enough stock! Only ' + stock + ' left.');
            }
        });

        const decreaseButton = document.createElement('button');
        decreaseButton.textContent = '-';
        decreaseButton.addEventListener('click', () => {
            if (item.quantity > 0) {
            item.quantity--;
            localStorage.setItem('cart', JSON.stringify(cartData));
            location.reload();
            }
        });

        if (item.quantity === 0) {
            const index = cartData.findIndex(cartItem => cartItem.id === id);
            if (index !== -1) {
                cartData.splice(index, 1);
                localStorage.setItem('cart', JSON.stringify(cartData));
                location.reload();
            }
        }

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
            const index = cartData.findIndex(cartItem => cartItem.id === id);
            if (index !== -1) {
                cartData.splice(index, 1);
                localStorage.setItem('cart', JSON.stringify(cartData));
                location.reload();
            }
        });
        quantityControls.appendChild(increaseButton);
        quantityControls.appendChild(decreaseButton);
        quantityControls.appendChild(deleteButton);
        itemElement.appendChild(quantityControls);
        cartItemsContainer.appendChild(itemElement);
        totalPrice += parseFloat(price) * parseInt(quantity);
    });
    
    totalPriceElement.textContent = `Total Price: $${totalPrice.toFixed(2)}`;
    const sortByNameButton = document.getElementById('sort-by-name');
    const sortByPriceButton = document.getElementById('sort-by-price');
    sortByNameButton.addEventListener('click', () => {
        cartData.sort((a, b) => a.name.localeCompare(b.name));
        localStorage.setItem('cart', JSON.stringify(cartData));
        location.reload();
    });
    sortByPriceButton.addEventListener('click', () => {
        cartData.sort((a, b) => a.price - b.price);
        localStorage.setItem('cart', JSON.stringify(cartData));
        location.reload();
    });
    
    let checkoutButton = document.getElementById('checkout-button');
    checkoutButton.onclick = function() {
        cartData = localStorage.getItem('cart');
        localStorage.removeItem('cart');
        location.reload();
        fetch('/storeapp/data_processing/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: cartData,
    })
    .then(response => {
        if (!response.ok)
            throw new Error('Error in fetch');
        return response.json();
    })
    .then(date =>{
        console.log('Response:', date);
    })
    .then(error=>{
        console.error('Error:', error);
        });
    }

    // let discountCodeContainer = document.getElementById('discount-code-container');
    // const discountCodeInput = document.createElement('input');
    // discountCodeInput.type = 'text';
    // discountCodeInput.placeholder = 'Enter discount code';
    // discountCodeInput.id = 'discount-code';
    // const applyDiscountButton = document.createElement('button');
    // applyDiscountButton.textContent = 'Apply Discount';
    // applyDiscountButton.addEventListener('click', () => {
    //     const discountCode = discountCodeInput.value.trim();
    //     if (discountCode === 'DISCOUNT10') {
    //         totalPrice *= 0.9; // Apply 10% discount
    //         totalPriceElement.textContent = `Total Price: $${totalPrice.toFixed(2)}`;
    //         alert('Discount applied!');
    //     } else {
    //         alert('Invalid discount code!');
    //     }
    // });

    // discountCodeContainer.appendChild(discountCodeInput);
    // discountCodeContainer.appendChild(applyDiscountButton);

});
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}