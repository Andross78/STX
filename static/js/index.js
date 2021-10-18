document.addEventListener("DOMContentLoaded", function(event) {

    console.log("DOM fully loaded and parsed");

    var secondInput = document.querySelector('#second_date')
    var selectFilter = document.querySelector('#filter_type')

    secondInput.disabled = true

    selectFilter.addEventListener('change',function(event){
        console.log(event.target.value)
        if (event.target.value == 'publish_date') {
            secondInput.removeAttribute('disabled')
        } else {
            if (secondInput.hasAttribute('disabled') === true) {

            } else {
                secondInput.setAttribute('disabled', 'disabled')
            }

        }
    })

});