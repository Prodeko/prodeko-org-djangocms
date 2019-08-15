$(document).ready(function() {
  var csrftoken = $('[name=csrfmiddlewaretoken]').val();
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });

  function showPolicy() {
    $('.policy-container').removeClass('d-none');
  }

  function hidePolicy() {
    $('.policy-container').addClass('d-none');
  }

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
    $('#id_has_accepted_policies').change(function() {
      if (this.checked) {
        acceptPolicy();
      } else {
        denyPolicy();
      }
    });

    $('#id_email').change(function() {
      if ($(this).val().length === 0) {
        acceptPolicy();
        hidePolicy();
      } else {
        showPolicy();
        denyPolicy();
      }
    });
  }

  var formContact = $('#form_contact');
  var hasAcceptedPolicies = true;
  registerEventListeners();

  formContact.on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(formContact.get(0));

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
        success: function(data) {
          // Google Analytics form submission tracking
          dataLayer.push({ event: 'formSubmitted', formName: 'form_contact' });
          document.write(data);
        },

        // Re-renders the same page with error texts.
        error: function(xhr) {
          if (xhr.status === 599) {
            // Google Analytics form error tracking
            dataLayer.push({ event: 'formError', formName: 'form_contact' });
            $('#form-contact-wrapper').replaceWith(xhr.responseText);
            $('button[type=submit]').removeAttr('disabled');
            registerEventListeners();
          }
        }
      });
    }
  });
});
