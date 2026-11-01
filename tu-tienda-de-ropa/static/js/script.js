document.addEventListener("DOMContentLoaded", function() {
    const cambiosBtn = document.querySelector(".button-change");
    const formContainer = document.getElementById("form-container");

    cambiosBtn.addEventListener("click", function(event) {
        event.preventDefault(); // Evitar el comportamiento predeterminado del enlace

        const formHTML = `
            <div class="modal">
                <div class="modal-content">
                    <span class="close-btn">&times;</span>
                    <div class="body-change">
                        <div class="conteiner-change">
                            <div class="title-change">FORMULARIO DE CAMBIO</div>
                            <form id="formu-validacion" novalidate>
                                <div class="form-send">
                                    <span>NUMERO DE PEDIDO *</span>
                                    <input type="text" placeholder="XX-XXXXXXXXXXXX" required>
                                    <small class="error-message">Ingrese el número de pedido</small>
                                </div>
                                <div class="form-send">
                                    <span>NOMBRE *</span>
                                    <input type="text" placeholder="Juan Lopéz" required>
                                    <small class="error-message">Ingrese el nombre</small>
                                </div>
                                <div class="form-send">
                                    <span>DNI *</span>
                                    <input type="number" placeholder="22333444" required>
                                    <small class="error-message">Ingrese el número de DNI</small>
                                </div>
                                <div class="form-send">
                                    <span>CORREO ELECTRONICO *</span>
                                    <input type="email" required>
                                    <small class="error-message">Ingrese el correo electrónico</small>
                                </div>
                                <div class="form-send">
                                    <span>ARTICULO A CAMBIAR *</span>
                                    <input type="text" required>
                                    <small class="error-message">Ingrese el artículo a cambiar</small>
                                </div>
                                <div class="form-send">
                                    <span>TIPO DE ENTREGA *</span>
                                    <select id="tipo-entrega" name="tipo-entrega" required>
                                        <option value="">Selecciona una opción</option>
                                        <option value="envio">Envío a domicilio</option>
                                        <option value="recogida">Retiro en sucursal</option>
                                    </select>
                                    <small class="error-message">Seleccione el tipo de entrega</small>
                                </div>
                                <div class="form-send">
                                    <span>ARTICULO NUEVO *</span>
                                    <input type="text" required>
                                    <small class="error-message">Ingrese el artículo nuevo</small>
                                </div>
                                <div class="form-send">
                                    <span>LINK NUEVO ARTICULO *</span>
                                    <input type="text" required>
                                    <small class="error-message">Ingrese el link del nuevo artículo</small>
                                </div>
                                <div class="button-container">
                                    <button type="submit">ENVIAR FORMULARIO</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `;

        formContainer.innerHTML = formHTML;

        const modal = document.querySelector(".modal");
        const closeButton = document.querySelector(".close-btn");
        const form = document.getElementById("formu-validacion");

        modal.style.display = "flex";

        closeButton.addEventListener("click", function() {
            modal.style.display = "none";
        });

        window.addEventListener("click", function(event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });

        form.addEventListener("submit", function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll("input, select");
            inputs.forEach(input => {
                const errorMessage = input.nextElementSibling;
                if (!input.checkValidity()) {
                    errorMessage.style.display = "block";
                    isValid = false;
                } else {
                    errorMessage.style.display = "none";
                }
            });
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
});
