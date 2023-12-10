// This is your test publishable API key.
const stripe = Stripe('pk_test_NMlBMUrHeQVCbjgLn3RZBDrO002kfqUCmn');

// The items the customer wants to buy
const items = [{ id: 'xl-tshirt' }];

let elements;

initialize();
checkStatus();

document
  .querySelector('#payment-form')
  .addEventListener('submit', handleSubmit);

// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch('/apply-membership/create-payment-intent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ items }),
  });
  const { clientSecret } = await response.json();

  const appearance = {
    theme: 'stripe',
  };
  elements = stripe.elements({ appearance, clientSecret });

  const paymentElementOptions = {
    layout: 'tabs',
  };

  const paymentElement = elements.create('payment', paymentElementOptions);
  paymentElement.mount('#payment-element');
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);
  submitForm();

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: 'http://localhost:4242/checkout.html',
      receipt_email: emailAddress,
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === 'card_error' || error.type === 'validation_error') {
    showMessage(error.message);
  } else {
    showMessage('An unexpected error occurred.');
  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    'payment_intent_client_secret'
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case 'succeeded':
      showMessage('Payment succeeded!');
      break;
    case 'processing':
      showMessage('Your payment is processing.');
      break;
    case 'requires_payment_method':
      showMessage('Your payment was not successful, please try again.');
      break;
    default:
      showMessage('Something went wrong.');
      break;
  }
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector('#payment-message');

  messageContainer.classList.remove('hidden');
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add('hidden');
    messageContainer.textContent = '';
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector('#submit').disabled = true;
    document.querySelector('#spinner').classList.remove('hidden');
    document.querySelector('#button-text').classList.add('hidden');
  } else {
    document.querySelector('#submit').disabled = false;
    document.querySelector('#spinner').classList.add('hidden');
    document.querySelector('#button-text').classList.remove('hidden');
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {
  var csrftoken = $('[name=csrfmiddlewaretoken]').val();
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    },
  });

  registerEventListeners();
});

var hasAcceptedPolicies = false;

function acceptPolicy() {
  $('button[type=submit]').removeAttr('disabled');
  $('#policy-not-accepted').fadeOut('fast');
  hasAcceptedPolicies = true;
}

function denyPolicy() {
  $('button[type=submit]').attr('disabled', '');
  $('#policy-not-accepted').fadeIn('fast');
  hasAcceptedPolicies = false;
}

function registerEventListeners() {
  $('#id_has_accepted_policies').change(function () {
    if (this.checked) {
      acceptPolicy();
    } else {
      denyPolicy();
    }
  });
}

function submitForm(e) {
  e.preventDefault();
  var formData = new FormData($('#form_apply').get(0));

  if (!hasAcceptedPolicies) {
    denyPolicy();
  } else {
    $('button[type=submit]').attr('disabled', '');
    $.ajax({
      url: '',
      type: 'POST',
      data: formData,
      contentType: false, // Indicates 'multipart/form-data'
      processData: false,
      success: function (data) {
        // Google Analytics form submission tracking
        dataLayer.push({ event: 'formSubmitted', formName: 'form_apply' });
        document.write(data);
      },

      // Re-renders the same page with error texts.
      error: function (xhr) {
        if (xhr.status === 599) {
          // Google Analytics form error tracking
          dataLayer.push({ event: 'formError', formName: 'form_apply' });
          $('#form-apply-wrapper').replaceWith(xhr.responseText);
          registerEventListeners();
          acceptPolicy();
        }
      },
    });
  }
}
