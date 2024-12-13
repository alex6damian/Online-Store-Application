document.addEventListener('DOMContentLoaded', function() {
    let cartData = localStorage.getItem('cart')
    const cartItemsContainer = document.getElementById('cart-items-container');
    const totalPriceElement = document.getElementById('total-price');
    let totalPrice = 0;
    cartData = cartData.split(',');
    cartItemsContainer.innerHTML = '';

    cartData.forEach(item => {
        console.log(item);
        const cartItem = document.createElement('div');
        JSON.parse(item)
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <p>${item.name}</p>
            <p>ID: ${item.id}</p>
            <p>Quantity: ${item.quantity}</p>
            <p>Price: ${item.price}</p>
        `;
        cartItemsContainer.appendChild(cartItem);
        totalPrice += item.price * item.quantity;
    });

    totalPriceElement.textContent = totalPrice;
});