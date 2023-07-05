$(document).ready(function () {
    const svg = document.getElementById("eye");
    const passwordInput = document.getElementById("id_usua_chpasusu");
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

    //****QUITAR LETRAS***
    const numeroDNI = document.getElementById("id_pers_chdocide");
    const numeroCel = document.getElementById("id_pers_chcelper");


    numeroDNI.addEventListener("keypress", function(event) {
      return soloNumeros(event, 8);
    });
    numeroCel.addEventListener("keypress", function(event) {
      return soloNumeros(event, 9);
    });
    
    function soloNumeros(event, maximo) {
        const teclaPresionada = event.key;
        const valorInput = event.target.value;
      
        if (
          (teclaPresionada < "0" || teclaPresionada > "9") ||
          valorInput.length >= maximo
        ) {
          event.preventDefault();
          return false;
        }
    }  
    
    //***FIN QUITAR LETRAS */

    // *****VALIDACIONES DE LOS CAMPOS****
    // const formulario1 = document.getElementById('step1');
    // const inputs1 = document.querySelectorAll('#step1 input');
    const expresiones = {
        nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
        apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
        dni: /^\d{8,8}$/, // 8 a 8 numeros.
        correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
        celular: /^\d{9,9}$/, // 9 numeros.
        usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
        password: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/ // min 6 digitos.
    }

    const campos = {
        nombre: false,
        apellido: false,
        dni: false,
        correo: false,
        direccion: false,
        celular: false,
        usuario: false,
        password: false
    }

    // function notificacion(inputmsg, inputmsgtext, msg) {
    //     inputmsg.removeClass('opacity-0');
    //     inputmsgtext.text(msg);
    //     setTimeout(function () {
    //         $('#error-message').addClass('opacity-0');
    //     }, 4000);
    // }

    const validarFormulario1 = (e) => {
        switch (e.attr("name")) {
            case "pers_chnomper":                
                validarCampo(expresiones.nombre, e.val(), 'nombre', 'ingrese nombre válido');
                break;
            case "pers_chapeper":                    
                validarCampo(expresiones.apellido, e.val(), 'apellido', 'ingrese apellido válido');
                break;
            case "pers_chdocide":
                validarCampo(expresiones.dni, e.val(), 'dni', 'ingrese dni válido');
                break;
            case "pers_chemaper":
                validarCampo(expresiones.correo, e.val(), 'correo', 'ingrese correo válido');
                break;
        }
    }
    const validarFormulario2 = (e) => {
        switch (e.attr("name")) {
            case "dire_chnomdir":
                validardireccion(e.val(), 'direccion');
                break;
            case "pers_chcelper":                
                validarCampo(expresiones.celular, e.val(), 'celular', 'ingrese número válido');
                break;
            case "usua_chlogusu":
                validarCampo(expresiones.usuario, e.val(), 'usuario', 'ingrese usuario válido');
                break;
            case "usua_chpasusu":
                validarCampo(expresiones.password, e.val(), 'password', 'min 6, use may. minús. y num.');
                // validarPassword2();
                break;
            // case "password2":
            //     validarPassword2();
            // break;
        }
    }

    const validarCampo = (expresion, input, campo, msg) => {
        
        if (input.trim()=='') {            
            campos[campo] = false;
            $("#error-text-" + campo).text('el campo esta vacío');
            $("#error-" + campo).removeClass("opacity-0");
            setTimeout(function () {
                $("#error-" + campo).addClass("opacity-0");
            }, 4000);
            return;
        }
        if (expresion.test(input)) {            
            campos[campo] = true;
        } else {
            campos[campo] = false;
            $("#error-text-" + campo).text(msg);
            $("#error-" + campo).removeClass("opacity-0");
            setTimeout(function () {
                $("#error-" + campo).addClass("opacity-0");
            }, 4000);
        }
    }

    const validardireccion=( input, campo)=>{
        if (input.trim()=='') {            
            campos[campo] = false;
            $("#error-text-" + campo).text('el campo esta vacío');
            $("#error-" + campo).removeClass("opacity-0");
            setTimeout(function () {
                $("#error-" + campo).addClass("opacity-0");
            }, 4000);            
        }
        else{
            campos[campo] = true;
        }
    }
    // *****FIN VALIDACIONES DE LOS CAMPOS****

    $("#step1 #next-button").click(function (event) {
        event.preventDefault();
        console.log("Form submitted");
        var nombre = $("#id_pers_chnomper");
        var apellido = $("#id_pers_chapeper");
        var dni = $("#id_pers_chdocide");
        var correo = $("#id_pers_chemaper");
        var nextButton1 = $(this);
        validarFormulario1(nombre);
        validarFormulario1(apellido);
        validarFormulario1(dni);
        validarFormulario1(correo);
        if (campos.nombre && campos.apellido && campos.dni && campos.correo) {            
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
        }


    });

    // ***FIN PASO 1***

    $("#step2 #enviar-btn").click(function (event) {
        event.preventDefault();
        console.log("Form submitted");
        var direccion = $("#id_dire_chnomdir");
        var celular = $("#id_pers_chcelper");
        var usuario = $("#id_usua_chlogusu");
        var password = $("#id_usua_chpasusu");
        validarFormulario2(direccion);
        validarFormulario2(celular);
        validarFormulario2(usuario);
        validarFormulario2(password);
        var enviarbtn = $(this);
        if (campos.direccion && campos.celular && campos.usuario && campos.password) {
            $.ajax({
                url: "/register/step2/",
                type: "POST",
                data: $("#step2").serialize(),
                beforeSend: function () {
                    enviarbtn.prop("disabled", true);
                    $("#spin-registrarse").removeClass("hidden");
                    $("#txt-registrarse").text("PROCESANDO...");
                },
                success: function (data) {
                    toastr.success("Redirigiendo al Inicio de Sesion...");
                    toastr.success("Registro Exitoso!");
                    setTimeout(function () {
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
                    enviarbtn.prop("disabled", false);
                    $("#spin-registrarse").addClass("hidden");
                    $("#txt-registrarse").text("REGISTRARSE");
                },
            });
        }
    });
});