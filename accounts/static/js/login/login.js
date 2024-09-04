const svg = document.getElementById("eye");
const passwordInput = document.getElementById("id_password");
let passwordVisible = false;

svg.addEventListener("click", function () {
    if (passwordVisible) {
        passwordInput.type = "password";
        passwordVisible = false;
        svg.style.fill = "";
    } else {
        passwordInput.type = "text";
        passwordVisible = true;
        svg.style.fill = "#1f2937";
    }
});
function showSpinner() {
    document.getElementById('load-modal').classList.remove('hidden');
    document.getElementById('load-modal').classList.add('flex');

}

window.onload = function () {
    hideSpinner();
}

function hideSpinner() {
    document.getElementById('load-modal').classList.remove('flex');
    document.getElementById('load-modal').classList.add('hidden');
};

$(document).ready(function () {

    $('#login-form').on('submit', function (event) {
        event.preventDefault();
        var username = $('#id_username').val().trim();
        var password = $('#id_password').val().trim();
  
        if (username === '' || password === '') {
        hideSpinner();
          $('#error-message').removeClass('opacity-0');
          $('#error-text').text('Campo(s) vacío(s)');
          setTimeout(function() {
            $('#error-message').addClass('opacity-0');
          }, 2000);
          return;
        }

        var formData = $(this).serialize();
        $.ajax({
            url: '/login/',
            type: 'POST',
            data: formData,
            success: function (response) {
                // alert('recibido correctamente');
                if (response.errorslog) {
                    hideSpinner();
                    var errorMessage = response.errorslog;
                    $('#error-message').removeClass('opacity-0');
                    $('#error-text').text(errorMessage);
                    setTimeout(function () {
                        $('#error-message').addClass('opacity-0');
                    }, 2000);
                } else {
                    
                    window.location.assign(response.url);
                }
            },
            error: function (xhr, error) {
                alert('Se produjo un error en la solicitud.');
            }
        });
    });
});