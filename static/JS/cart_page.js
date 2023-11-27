function orderCart() {
    fetch('/order_cart', {
        method: 'POST',
    })
    .then(response => {
        if (response.ok) {
            window.location.href = window.location.origin + "/my_orders";
        } else {
            // Handle errors if needed
            toastr.error("Faild to complete the order");
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}