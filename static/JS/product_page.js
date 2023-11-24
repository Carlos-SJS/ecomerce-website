function changeMainImage(imageUrl) {
    document.getElementById('main-img').src = imageUrl;
}

function addToCart(){
    var url = window.location.origin + "/addtocart";

    
    const urlParams = new URLSearchParams(window.location.search);

    const data = new URLSearchParams();
    data.append('productid', urlParams.get("id"));
    data.append('count', 1);

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: data
    })
}