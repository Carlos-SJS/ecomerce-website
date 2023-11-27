var stars = 5;
function submitReview(){
    var title = document.getElementById("rev-title").value;
    var content = document.getElementById("rev-content").value;

    var url = window.location.origin + "/submit_review";

    
    const urlParams = new URLSearchParams(window.location.search);
    const data = new URLSearchParams();
    data.append('productid', urlParams.get("id"));
    data.append('title', title);
    data.append('content', content);
    data.append('stars', stars);

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: data
    }).then(response => {
        if (response.ok) {
            location.reload();
        } else {
            toastr.error("No se pudo publicar tu review");
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

function setStars(number){
    stars = number;
    var st1 = document.getElementById("st5");
    var st2 = document.getElementById("st4");
    var st3 = document.getElementById("st3");
    var st4 = document.getElementById("st2");
    var st5 = document.getElementById("st1");
    if (st1.classList.contains('selected')) {
        st1.classList.remove('selected');
    }
    if (st2.classList.contains('selected')) {
        st2.classList.remove('selected');
    }
    if (st3.classList.contains('selected')) {
        st3.classList.remove('selected');
    }
    if (st4.classList.contains('selected')) {
        st4.classList.remove('selected');
    }
    if (st5.classList.contains('selected')) {
        st5.classList.remove('selected');
    }

    if(stars < 1){
        st1.classList.add('selected');
    }
    if(stars < 2){
        st2.classList.add('selected');
    }
    if(stars < 3){
        st3.classList.add('selected');
    }
    if(stars < 4){
        st4.classList.add('selected');
    }
    if(stars < 5){
        st5.classList.add('selected');
    }
}