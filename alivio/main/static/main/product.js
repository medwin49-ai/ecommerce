
function product_price(){

  var selectBox = document.getElementById("selectBox");
 
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  console.log(selectedValue)
  
  var price = document.getElementById("potency_price");

  price.innerText = "Price: $" +selectedValue; 
}
