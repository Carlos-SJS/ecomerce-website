var productImages = [];

function dropHandler(event) {
    event.preventDefault();

    if (event.dataTransfer.items) {
        for (var i = 0; i < event.dataTransfer.items.length; i++) {
            if (event.dataTransfer.items[i].kind === 'file') {
                var file = event.dataTransfer.items[i].getAsFile();
                displayImage(file);
                uploadImage(file);
            }
        }
    }
}

function dragOverHandler(event) {
    event.preventDefault();
}

var createdImgs = 0;

function displayImage(file) {
    var reader = new FileReader();

    reader.onload = function (e) {
        if(createdImgs == 0){
            var img_div = document.getElementById('main-image');
            var new_img = document.createElement('img');
            new_img.src = e.target.result;
            img_div.appendChild(new_img);
        }
        var img_div = document.getElementById('thumbnail-column');
        var new_img = document.createElement('img');
        new_img.src = e.target.result;

        img_div.appendChild(new_img);
        createdImgs+=1;
    };

    reader.readAsDataURL(file);
}

function uploadImage(file) {
    productImages.push(file.name);
    var formData = new FormData();
    formData.append('file', file);

    fetch('/upload_image', {
        method: 'POST',
        body: formData
    })
}

function createProduct(){
    var url = window.location.origin + "/create_product";

    var prodName = document.getElementById('ProdName').value;
    var shortDesc = document.getElementById('ShortDescription').value;
    var fullDesc = document.getElementById('FullDescription').value;
    var price = parseFloat(document.getElementById('ProdPrice').value, 10);
    var stock = parseInt(document.getElementById('ProdStock').value, 10);
    var categories = document.getElementById('ProdCat').value;

    if(isNaN(price)){
        toastr.error("The product price is invalid");
    }
    if(isNaN(stock)){
        toastr.error("The product stock is invalid");
    }

    const data = new URLSearchParams();
    productImages.forEach((item, index) => {
        data.append('image', item);
    });

    data.append('name', prodName);
    data.append('short_desc', shortDesc);
    data.append('full_desc', fullDesc);
    data.append('price', price);
    data.append('stock', stock);
    data.append('categories', categories);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data
    })

    toastr.success('El producto ha sido creado correctamente');
}