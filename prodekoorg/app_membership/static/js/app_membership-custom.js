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

  function removeReceiptName(e) {
    e.target.parentElement.previousElementSibling.value = '';
    $(e.target.parentElement).remove();
  }

  function showFileName(e) {
    var input = e.target;
    var filename = input.files[0].name;

    var span = document.createElement('span');
    span.classList.add('form-text', 'receipt-name', 'pr-2');
    span.innerHTML = `<i id="removeReceptIcon" class="fas fa-minus-square fa-lg pr-2"></i> ${filename}`;
    span.firstElementChild.addEventListener('click', removeReceiptName);

    var parentNode = input.parentNode;
    if (parentNode.children.length > 2) {
      parentNode.removeChild(parentNode.children[2]);
    }
    parentNode.appendChild(span);
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
    $('#id_has_accepted_policies').change(function () {
      if (this.checked) {
        acceptPolicy();
      } else {
        denyPolicy();
      }
    });

    $('#id_receipt').change(showFileName);
  }

  var formApply = $('#form_apply');
  var hasAcceptedPolicies = false;
  registerEventListeners();

  formApply.on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(formApply.get(0));

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
  });
});
