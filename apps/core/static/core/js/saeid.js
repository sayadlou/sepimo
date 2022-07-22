function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function productListFormSend(e) {
    event.preventDefault();
    var filterFormData = $('#filter-form').serialize()
    var sortFormData = $('#sort-form').serialize()
    var url = window.location.pathname + "?" + sortFormData + "&" + filterFormData
    window.location.replace(url)
}