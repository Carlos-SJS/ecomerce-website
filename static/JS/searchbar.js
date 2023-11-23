function search(){
    var params = new URLSearchParams(window.location.search);
    var search_querry = document.getElementById("search_field").value;
    params.set("Search", encodeURIComponent(search_querry));
    var querry_string = params.toString();

    var newURL = window.location.origin + "/products?" +querry_string;
    window.location.href = newURL;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("search_field").addEventListener("keydown", function (e) {
        if (e.code === "Enter") {
            search();
        }
    })
 }, false);