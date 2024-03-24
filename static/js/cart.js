// Update cart functionality
let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user); // Access the user variable

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

// Function to add items to the cart using cookies
function addCookieItem(productId, action) {
    console.log('not logged in');

    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('remove item');
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    location.reload();
}

// Function to update user's order
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    let url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    });
}

// Function to update cart number display
function updateCartNumber(cartItems) {
    document.getElementById('cart-number').innerText = cartItems;
}

// Add-to-cart button functionality
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.dataset.productId;
        const action = 'add';

        fetch('/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                productId: productId,
                action: action
            })
        })
        .then(response => response.json())
        .then(data => {
            updateCartNumber(data.cartItems);
        });
    });
});

// Function to clear the cart
function clearCart() {
    const action = 'clear';   // Specify the action as 'clear'

    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            productId: null,  // No need to specify productId for clearing the cart
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart cleared.');
        // Optionally, you can update the cart number display or perform any other action after clearing the cart
    })
    .catch(error => {
        console.error('Error clearing cart:', error);
    });
}


