$(document).ready(function() {
    const svg = document.getElementById("eye");
    const passwordInput = document.getElementById("id_usua_chpasusu");
    let passwordVisible = false;

    svg.addEventListener("click", function() {
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


    $("#step1 #next-button").click(function() {
        //event.preventDefault();
        console.log("Form submitted");
        var nextButton1 = $(this);
        $.ajax({
            url: "/register/",
            type: "POST",
            data: $("#step1").serialize(),
            beforeSend: function () {                    
            nextButton1.prop("disabled", true);
            $("#spin1-registrarse").removeClass("hidden");
            $("#txt1-registrarse").text("PROCESANDO...");
            },
            success: function (data) {
            var stepsContainer = $("#steps");          
            stepsContainer.fadeOut("fast", function () {
                $("#step1").hide();
                $("#step2").show();
                stepsContainer.fadeIn("fast");
            });          
            },
            error: function (xhr, status, error) {
            // Mostrar un mensaje de error al usuario
            if (xhr.status === 400) {
                toastr.error(xhr.responseText);
            } else {
                // Mostrar un mensaje de error genérico
                alert("Error: " + error);
            }
            },
            complete: function () {                    
            nextButton1.prop("disabled", false);
            $("#spin1-registrarse").addClass("hidden");
            $("#txt1-registrarse").text("CONTINUAR");
            },
        });


    });

    $("#step2 #enviar-btn").click(function() {
        //event.preventDefault();
        console.log("Form submitted");
        //var nextButton1 = $(this);
        $.ajax({
            url: "/register/step2/",
            type: "POST",
            data: $("#step2").serialize(),
            beforeSend: function () {                    

            },
            success: function (data) {
                toastr.success("Redirigiendo al Inicio de Sesion...");
                toastr.success("Registro Exitoso!");
                setTimeout(function() {
                    window.location.href = "/login/";  // Reemplaza con la URL de la página de inicio de sesión
                }, 2000);  //
            },
            error: function (xhr, status, error) {
            // Mostrar un mensaje de error al usuario
            if (xhr.status === 400) {
                toastr.error(xhr.responseText);
            } else {
                // Mostrar un mensaje de error genérico
                alert("Error: " + error);
            }
            },
            complete: function () {                    
            // nextButton1.prop("disabled", false);
            // $("#spin1-registrarse").addClass("hidden");
            // $("#txt1-registrarse").text("CONTINUAR");
            },
        });
    });
});