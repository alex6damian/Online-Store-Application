window.onload = function() {
    let buttons = document.getElementsByClassName('add-to-cart');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    for (let btn of buttons) {
        let productId = btn.dataset['id'];
        if (cart.find(item => item.id === productId)) {
            btn.style.backgroundColor = 'grey';
        }
    }
    for (let btn of buttons) {
        btn.onclick = function() {
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            let productId = this.dataset['id'];
            let productName = this.dataset['name'];
            let productPrice = this.dataset['price'];
            let productStock = this.dataset['stock'];
            let existingProduct = cart.find(item => item.id === productId);

            if (existingProduct) {
                alert('Product is already in cart!'); // Alert user
            } else if(productStock > 0) {
                let product = {
                    id: productId,
                    name: productName,
                    price: productPrice,
                    quantity: 1,
                    stock: productStock
                };
                btn.style.backgroundColor = 'grey';
                btn.disabled = true;
                cart.push(product);
                localStorage.setItem('cart', JSON.stringify(cart)); // Update cart
            }
        }
    }
}
