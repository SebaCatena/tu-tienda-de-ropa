let btnSend = document.querySelector("#btn-send");

// Expresiones regulares
let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Escuchar un evento
btnSend.addEventListener('click', function(event) {
    // Prevenir el envío del formulario si hay errores
    event.preventDefault();

    // Obtener los campos del formulario
    let firstname = document.querySelector("#firstname");
    let lastname = document.querySelector("#lastname");
    let email = document.querySelector("#email");

    // Borrar mensajes de error previos
    document.querySelector("#error-firstname").innerHTML = "";
    document.querySelector("#error-lastname").innerHTML = "";
    document.querySelector("#error-email").innerHTML = "";

    let isValid = true;

    // Validar el campo Nombre
    if (firstname.value.trim() === '' || firstname.value.trim().length < 3) {
        document.querySelector("#error-firstname").innerHTML = "completar el campo Nombre";
        isValid = false;
    }

    // Validar el campo Apellido
    if (lastname.value.trim() === '') {
        document.querySelector("#error-lastname").innerHTML = "completar campo Apellido";
        isValid = false;
    }

    // Validar el campo Email
    if (!emailRegex.test(email.value)) {
        document.querySelector("#error-email").innerHTML = "email formato inválido";
        isValid = false;
    }

    // Si todos los campos son válidos, enviar el formulario
    if (isValid) {
        alert('Los datos fueron enviados...');
        
         document.querySelector("#formRegister").submit();
    }
});