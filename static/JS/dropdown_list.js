let list_headers = document.querySelectorAll('div.list-header');

list_headers.forEach(l_header => {
    l_header.addEventListener('click', (e) => {
        const list_item_data = l_header.nextElementSibling;

        list_item_data.style.setProperty('--openHeight', list_item_data.scrollHeight + 'px');

        list_item_data.classList.toggle('show');
        list_item_data.classList.toggle('hide');


        l_header.classList.toggle('show');
        l_header.classList.toggle('hide');
    })
});
