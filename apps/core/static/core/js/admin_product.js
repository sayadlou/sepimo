function doWork() {
    var priceField = document.getElementsByClassName('field-price').item(0)
    var variantTitleField = document.getElementsByClassName('field-variant_title').item(0)
    var hasVariant = document.getElementById('id_has_variant')
    var variantSetGroup = document.getElementById('variant_set-group')
    onHasVariantChange()
    hasVariant.addEventListener('change', onHasVariantChange)

    function onHasVariantChange() {
        if (hasVariant.checked) {
            variantSetGroup.style.display = 'block'
            variantTitleField.style.display = 'block'
            priceField.style.display = 'none'
        } else {
            variantSetGroup.style.display = 'none'
            variantTitleField.style.display = 'none'
            priceField.style.display = 'block'
        }
    }
}

window.addEventListener("load", doWork);