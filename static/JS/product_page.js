function changeMainImage(imageUrl) {
    document.getElementById('main-img').src = imageUrl;
}

function addToCart(){
    var url = window.location.origin + "/addtocart";

    
    const urlParams = new URLSearchParams(window.location.search);

    const data = new URLSearchParams();
    data.append('productid', urlParams.get("id"));
    data.append('count', document.getElementById('cart_count').value);

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: data
    })

    toastr.success('El producto ha sido añadido a tu carrito ');
}

function increment(max_count) {
    var input = document.getElementById('cart_count');
    input.value = Math.min(parseInt(input.value, 10) + 1, max_count);
}

function decrement() {
    var input = document.getElementById('cart_count');
    if (parseInt(input.value, 10) > 1) {
        input.value = parseInt(input.value, 10) - 1;
    }
}