var updatePop= document.getElementsByClassName('pop_button')

for(var i = 0; i< updatePop.length; i++){
updatePop[i].addEventListener('click', function(){
    var productId =  this.dataset.product_id
    productName = this.dataset.product_name
    productDescription = this.dataset.product_description
    productPrice = this.dataset.product_price
    productImage = this.dataset.image

    image_location = document.getElementById('popup_image')
    description_location = document.getElementById('popup_description')
    add_cart_location = document.getElementById('cart_button')
    wishlist_location = document.getElementById('wishlist_button')
    price_location = document.getElementById('popup_price')


    document.getElementById("popup_title").innerHTML =  productName ;

    var img = document.createElement("img");
    img.src = productImage;
    img.style.width = "35%";
    img.style.minWidth = "210px";
    img.style.height = "40%";
    img.style.minHeight = "230px";
    img.style.float = "left";
    img.style.padding = "10px";
    image_location.innerHTML = "";
    image_location.appendChild(img)

    description_location.innerHTML = productDescription

    add_cart_location.innerHTML = this.dataset.cart_button

    // Change the following according to wishlist backend, dummy button- functions as add to cart
    wishlist_location.innerHTML = '<button data-product="' + productId +'" data-action="add" class="btn btn-outline-secondary add-btn update-cart">Add to Wishlist</button>'

    price_location.innerHTML = '<h4 style="display: inline-block; float:right">Price: <strong>&#8377;' + productPrice + '</strong></h4>'

})}

function togglePopup(){           
    document.getElementById("popup-1").classList.toggle("active");           
}