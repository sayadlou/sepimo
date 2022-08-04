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

// add-cart-plus
function addCartMinusOnClick() {
    var cartValue = document.getElementById("cart-value")
    var value = parseInt(cartValue.value) - 1
    cartValue.value = value.toString();
}

function addCartPlusOnClick() {
    var cartValue = document.getElementById("cart-value")
    var value = parseInt(cartValue.value) + 1
    cartValue.value = value.toString();
}

function reviewSubmitOnClick() {
    event.preventDefault()
    formData = FormData()
    $.ajax({
        type: "POST",
        url: "process.php",
        data: formData,
        dataType: "json",
        encode: true,
    }).done(function (data) {
        console.log(data);
    });

}

function cartDeleteOnClick(e) {
    event.preventDefault();
    console.log(event.target.dataset.pk)
    var csrftoken = getCookie('csrftoken');

    var postData = {
        product: event.target.dataset.pk,
        type: 'premium'
    }
    $.ajax({
        url: event.target.dataset.url,
        type: 'post',
        data: postData,
        headers: {'X-CSRFToken': csrftoken},

    })
        .done(
            function (response) {
                alert("success");
                console.log(response)
            })
        .fail(
            function (response) {
                console.log(response)
            });


    // $.post(event.target.dataset.url, data)
    //     .done(
    //         function (response) {
    //             alert("success");
    //             console.log(response)
    //         })
    //     .fail(
    //         function (response) {
    //             console.log(response)
    //         });

}

function cartAddOnclick() {
    event.preventDefault();
    console.log($('#cart-add').serialize())
    var csrftoken = getCookie('csrftoken');
    console.log(event.target.dataset.cartwidget)
    var cartWidgetUrl = event.target.dataset.cartwidget
    var postData = $('#cart-add').serialize();
    $("#main-page").addClass("pgage-deactive")
    $.ajax({
        url: $('#cart-add').attr('action'),
        type: 'post',
        data: postData,
        headers: {'X-CSRFToken': csrftoken},

    })
        .done(
            function (response) {

                $.ajax({
                    url: cartWidgetUrl,
                    type: 'get',
                    headers: {'X-CSRFToken': csrftoken},
                })
                    .done(
                        function (response) {
                            $("#main-page").removeClass("pgage-deactive")
                            $("#cart-widget-div").html(response)
                            alertify.success("محصول به سبد اضافه شد");
                        }
                    ).fail(
                    function (response) {
                        location.reload()
                    }
                )
            })
        .fail(
            function (response) {
                $("#main-page").removeClass("pgage-deactive")
                alertify.warning("محصول به سبد اضافه نشد");
                console.log(response)
            });


}
