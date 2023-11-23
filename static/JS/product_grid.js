function redirectProduct(pId){
    var newURL = window.location.origin + "/product?id=" + pId;
    window.location.href = newURL;
}