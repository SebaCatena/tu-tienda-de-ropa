/*abrir y cerrar parte comprar/

const cartIcon = document.querySelector("#cart-icon");
const cart = document.querySelector(".cart");
const closeCart = document.querySelector("#cart-close");

cartIcon.addEventListener("click", () => {
    cart.classList.add("active");
});

closeCart.addEventListener("click", () => {
    cart.classList.remove("active")
});


//comienza cuando el documento este listo

if(document.readyState == "loading"){
    document.addEventListener("DOMContentLoaded", start);
}else{
    start();
}

//comenzar

function start(){
    addEvents();
}

//comenzar y volver a presentar

function update(){
    addEvents();
    updateTotal();
}

//eventos

function addEvents(){
    //quitar articulos

    let cartRemove_btns = document.querySelectorAll(".cart-remove");

    console.log(cartRemove_btns);

    cartRemove_btns.forEach((btn)=> {
        btn.addEventListener("click", handle_removeCartItem);
    });
    //modificar contador de articulo

    let cartQuantity_inputs = document.querySelectorAll(".cart-quantity");

    cartQuantity_inputs.forEach((input)=> {
        input.addEventListener("change",handle_changeItemQuantity);
    })

    //agregar articulos al carrito

    let addCart_btns = document.querySelectorAll(".add-Cart");
    addCart_btns.forEach((btn) => {
        btn.addEventListener("click", handle_addCartItem);
    });
}

//comprar

const buy_btn = document.querySelector(".btn-buy");
buy_btn.addEventListener("click", handle_buyOrden);


//eventos 

let itemsAdded = [];


function handle_addCartItem(){
    let product = this.parentElement;
    let title = product.querySelector(".product-title").innerHTML;
    let price = product.querySelector(".product-price").innerHTML;
    let imgSrc = product.querySelector(".product-img").src;

    console.log(title, price, imgSrc);

    let newToAdd = {
        title,
        price,
        imgSrc,
    };

    // Manejo del elemento existente
    if (itemsAdded.find((el) => el.title == newToAdd.title)){
        alert("Este artículo ya existe");
        return;
    } else {
        itemsAdded.push(newToAdd);
    }

    // Agregar productos al carrito
    
    let carBoxElement = cartBoxComponent(title,price,imgSrc);
    let newNode = document.createElement("div");
    newNode.innerHTML = carBoxElement;
    const cartContent = document.querySelector(".cart-content");
    cartContent.appendChild(newNode);

    // Agregar botón de eliminar
    let removeButton = document.createElement("i");
    removeButton.classList.add("bx", "bxs-trash-alt", "cart-remove");
    newNode.appendChild(removeButton);

    update();
}

function handle_removeCartItem(){
    this.parentElement.remove();    

    itemsAdded = itemsAdded.filter(
        (el) => 
        el.title != this.parentElement.querySelector(".cart-product-title").innerHTML);

    update();
}

function handle_changeItemQuantity()  {
        if (isNaN(this.value) || this.value < 1) {
            this.value = 1;
        }
        this.value = Math.floor(this.value); //mantiene numero entero

        update();
    }  


 function handle_buyOrden(){
    if (itemsAdded.length <= 0){
        alert("No hay pedido, realice uno primeramente");
        return;
    }

    const cartContent = cart.querySelector(".cart-content");
    cartContent.innerHTML = "";
    alert ("Pedido realizado con exito");
    itemsAdded = [];
    update();
}


//funciones de actualizar y render izar


function updateTotal(){
    let cartBoxes = document.querySelectorAll(".cart-box");
    const totalElement = cart.querySelector(".total-price");
    let total = 0;

    cartBoxes.forEach((cartBox) => {
        let priceElement = cartBox.querySelector(".cart-price");
        let price = parseFloat(priceElement.innerHTML.replace("$", ""));
        let quantity = cartBox.querySelector(".cart-quantity").value;
        
        total += price * quantity;
    });


    total = total.toFixed(2);//dos digitos despues del punto decimal

    totalElement.innerHTML = "$" + total;
}


function cartBoxComponent(title, price, imgSrc){

    return `
    
    <div class="cart-box">

      <img src=${imgSrc} alt="" class="cart-img">

      <div class="detail-box">

      <div class="cart-product-title"> ${title}</div>

      <div class="cart-price">${price}</div>
      <input type="number" value="1" class="cart-quantity">

      <div>

      <i class='bx bxs-trash-alt cart-remove'></i>

      </div> `;

}*/