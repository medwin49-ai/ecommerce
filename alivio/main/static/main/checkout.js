// Example starter JavaScript for disabling form submissions if there are invalid fields

(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {      
          if (!form.checkValidity()) {       
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()

console.log(globalVars['order'])
console.log("hello")


const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var stripe = Stripe("pk_test_51JIK9kAAyihVYZDS587CfyBK4VH5C0bInmrlwZvjbvy6ozXyOoqxR17TQZ5aT0cFXFUOuNS3Fy4f4Vn5lMrZ36m3006CKkKjAM");

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

var elements = stripe.elements();
var style = {
  base: {
    color: "#32325d",
    fontFamily: 'Arial, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#32325d"
    }
  },
  invalid: {
    fontFamily: 'Arial, sans-serif',
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");
card.on("change", function (event) {
  // Disable the Pay button if there are no card details in the Element
  document.querySelector("button").disabled = event.empty;
  document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
});


var form = document.getElementById("payment-form");
form.addEventListener("submit", function(event) {
  event.preventDefault();
  console.log("went thru here");
  // Complete payment when the submit button is clicked
  fetch("/create-payment-intent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      firstName: document.getElementById('firstName').value,
      lastName: document.getElementById('lastName').value,
      email: document.getElementById('email').value,
      address1: document.getElementById('address').value,
      address2: document.getElementById('address2').value,
      city: document.getElementById('city').value,
      state: document.getElementById('state').value,
      zip: document.getElementById('zip').value,
      order: globalVars['order']
    })
  })
    .then(function(result) {
      return result.json();
    })
    .then(function(data) {
      payWithCard(stripe, card, data.clientSecret);
    });
});

// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
var payWithCard = function(stripe, card, clientSecret) {
  loading(true);
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function(result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message);
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id);

      }
    });
};

/* ------- UI helpers ------- */

// Shows a success message when the payment is complete
var orderComplete = function(paymentIntentId) {
  
  loading(false);
  
  // var url = '/success';
  // var form = $('<form action="' + url + '" method="post">' +
  // '<input type="hidden" name="api_url" value="' + Return_URL + '" />' +
  // '</form>');
  // $('body').append(form);
  // form.submit();

  document.getElementById('success_form').submit();

};

// Show the customer the error from Stripe if their card fails to charge
var showError = function(errorMsgText) {
  loading(false);
  var errorMsg = document.querySelector("#card-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function() {
    errorMsg.textContent = "";
  }, 4000);
};

// Show a spinner on payment submission
var loading = function(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } 
  else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};
