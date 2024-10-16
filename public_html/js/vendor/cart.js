let cart = [];

// Function to add product to cart
function addToCart(product) {
    const existingProductIndex = cart.findIndex(item => item.id === product.id);

    if (existingProductIndex !== -1) {
        // Update quantity if product already exists in cart
        cart[existingProductIndex].quantity += 1;
    } else {
        product.quantity = 1;
        cart.push(product);
    }

    // Save cart to localStorage
    localStorage.setItem('shoppingCart', JSON.stringify(cart));

    // Update cart display across all pages
    updateCartDisplay();
}

// Function to update the cart display on all pages
function updateCartDisplay() {
    const cartList = document.querySelector('.cart_list');
    const cartItemsCount = document.querySelector('.cart_items_count');
    const cartTotalAmount = document.querySelector('.cart_total_amount');
    const topPanelCartButton = document.querySelector('.top_panel_cart_button');

    cartList.innerHTML = ''; // Clear current cart items
    let totalItems = 0;
    let totalAmount = 0;

    if (cart.length === 0) {
        cartList.innerHTML = '<li class="empty">No products in the cart.</li>';
    } else {
        cart.forEach(product => {
            totalItems += product.quantity;
            totalAmount += product.quantity * product.price;

            cartList.innerHTML += `
                <li class="cart_item">
                    <span>${product.name}</span> - <span>Quantity: ${product.quantity}</span>
                    <button class="remove_item" onclick="removeFromCart(${product.id})">Remove</button>
                </li>
            `;
        });
    }

    // Update item count and total price
    cartItemsCount.innerText = totalItems;
    topPanelCartButton.setAttribute('data-items', totalItems);
    cartTotalAmount.innerText = `LKR ${totalAmount.toFixed(2)}`;
    topPanelCartButton.setAttribute('data-summa', `LKR ${totalAmount.toFixed(2)}`);
}

// Function to remove item from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);

    // Update cart display and localStorage
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
    updateCartDisplay();
}

// Function to load cart from localStorage when page loads
function loadCart() {
    const savedCart = JSON.parse(localStorage.getItem('shoppingCart'));
    if (savedCart) {
        cart = savedCart;
        updateCartDisplay();
    }
}

// Load cart when the page loads
window.onload = loadCart;