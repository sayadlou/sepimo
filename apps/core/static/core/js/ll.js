jQuery(function (s) {
    s(".woocommerce-ordering").on("change", "select.orderby", function () {
        s(this).closest("form").trigger("submit")
    }), s("input.qty:not(.product-quantity input.qty)").each(function () {
        var o = parseFloat(s(this).attr("min"));
        0 <= o && parseFloat(s(this).val()) < o && s(this).val(o)
    });
    var e = "store_notice" + (s(".woocommerce-store-notice").data("noticeId") || "");
    "hidden" === Cookies.get(e) ? s(".woocommerce-store-notice").hide() : s(".woocommerce-store-notice").show(), s(".woocommerce-store-notice__dismiss-link").on("click", function (o) {
        Cookies.set(e, "hidden", {path: "/"}), s(".woocommerce-store-notice").hide(), o.preventDefault()
    }), s(".woocommerce-input-wrapper span.description").length && s(document.body).on("click", function () {
        s(".woocommerce-input-wrapper span.description:visible").prop("aria-hidden", !0).slideUp(250)
    }), s(".woocommerce-input-wrapper").on("click", function (o) {
        o.stopPropagation()
    }), s(".woocommerce-input-wrapper :input").on("keydown", function (o) {
        var e = s(this).parent().find("span.description");
        if (27 === o.which && e.length && e.is(":visible")) return e.prop("aria-hidden", !0).slideUp(250), o.preventDefault(), !1
    }).on("click focus", function () {
        var o = s(this).parent(), e = o.find("span.description");
        o.addClass("currentTarget"), s(".woocommerce-input-wrapper:not(.currentTarget) span.description:visible").prop("aria-hidden", !0).slideUp(250), e.length && e.is(":hidden") && e.prop("aria-hidden", !1).slideDown(250), o.removeClass("currentTarget")
    }), s.scroll_to_notices = function (o) {
        o.length && s("html, body").animate({scrollTop: o.offset().top - 100}, 1e3)
    }, s('.woocommerce form .woocommerce-Input[type="password"]').wrap('<span class="password-input"></span>'), s(".woocommerce form input").filter(":password").parent("span").addClass("password-input"), s(".password-input").append('<span class="show-password-input"></span>'), s(".show-password-input").on("click", function () {
        s(this).hasClass("display-password") ? s(this).removeClass("display-password") : s(this).addClass("display-password"), s(this).hasClass("display-password") ? s(this).siblings(['input[type="password"]']).prop("type", "text") : s(this).siblings('input[type="text"]').prop("type", "password")
    })
});