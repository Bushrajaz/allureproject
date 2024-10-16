// checkout.js
document.addEventListener("DOMContentLoaded", function() {
    const cartItemsDiv = document.getElementById('cart-items');
    const cartTotalDiv = document.getElementById('cart-total');

    let cartItems = JSON.parse(localStorage.getItem('cart')) || [];

    let total = 0;
    cartItemsDiv.innerHTML = cartItems.map(item => {
        total += item.price * item.quantity;
        return `
            <p><strong>${item.name}</strong> - ${item.quantity} x LKR ${item.price} = LKR ${item.price * item.quantity}</p>
        `;
    }).join('');

    cartTotalDiv.innerHTML = `<h3>Total: LKR ${total}</h3>`;
});

document.getElementById('checkout-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Order placed successfully!');
    localStorage.removeItem('cart');
    window.location.href = "thank_you.html"; // Redirect to a thank you page
});