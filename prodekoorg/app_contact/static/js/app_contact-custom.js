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
    $('button[type=submit]').prop('disabled', true);
  }

  function hidePolicy() {
    $('.policy-container').addClass('d-none');
    $('#id_has_accepted_policies').prop('checked', false);
    $('button[type=submit]').prop('disabled', false);
  }

  function acceptPolicy() {
    $('button[type=submit]').prop('disabled', false);
    $('#policy-not-accepted').fadeOut('fast');
    hasAcceptedPolicies = true;
  }

  function denyPolicy() {
    $('button[type=submit]').prop('disabled', true);
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

    $('#id_email').blur(function() {
      if ($(this).val().length === 0) {
        acceptPolicy();
        hidePolicy();
        counter = 0;
      } else {
        if (counter === 0) {
          showPolicy();
          counter += 1;
        }
        if (!hasAcceptedPolicies) {
          denyPolicy();
        }
      }
    });

    $('#id_contact_emails').change(function() {
      if ($(this).val() === 'PT') {
        $("label[for='id_message']").text(
          gettext(
            'What are you applying the money for? Alternatively, what could the board of Prodeko use the money for?'
          )
        );
      } else {
        $("label[for='id_message']").text(gettext('Your message'));
      }
    });
  }

  function initFormState() {
    counter = 0;

    // Reset checkbox
    $('#id_has_accepted_policies').prop('checked', false);

    if ($('#id_email').val().length > 0) {
      showPolicy();
      $('button[type=submit]').prop('disabled', true);
    } else {
      hidePolicy();
      $('button[type=submit]').prop('disabled', false);
    }

    // Show correct labels
    if ($('#id_contact_emails').val() === 'PT') {
      $("label[for='id_message']").text(
        gettext(
          'What are you applying the money for? Alternatively, what could the board of Prodeko use the money for?'
        )
      );
    } else {
      $("label[for='id_message']").text(gettext('Your message'));
    }
  }

  var formContact = $('#form_contact');
  var hasAcceptedPolicies = true;
  var counter = 0;
  registerEventListeners();
  initFormState();

  formContact.on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(formContact.get(0));

    if (!hasAcceptedPolicies) {
      denyPolicy();
    } else {
      $('button[type=submit]').prop('disabled', true);
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
            registerEventListeners();
            initFormState();
          }
        }
      });
    }
  });
});
