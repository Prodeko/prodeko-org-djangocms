$(document).ready(function () {
  /* Submit main-form */
  $('#main-form').on('submit', function (event) {
    event.preventDefault();
    $('.error').remove();
    var form = $(this);
    var formData = new FormData(form[0]);
    $.ajax({
      url: form.attr('action'),
      data: formData,
      type: 'POST',
      async: true,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response.success) {
          location.reload();
        } else {
          for (var key in response.errors.user_form) {
            var errorElement =
              '<div class="error alert alert-danger">' +
              response.errors.user_form[key] +
              '</div>';
            $('input[name=user_form-' + key + ']').after(errorElement);
          }

          for (key in response.errors.person_form) {
            errorElement =
              '<div class="error alert alert-danger">' +
              response.errors.person_form[key] +
              '</div>';
            $('input[name=person_form-' + key + ']').after(errorElement);
          }
        }
      },
    });
    return false;
  });

  /* get delete modal contents */
  $('.delete-link').on('click', function (event) {
    event.preventDefault();
    var modal = $($(this).attr('modal'));
    var url = $(this).attr('url');
    $.get(url, function (data) {
      modal.find('.modal-content').html(data);
    });
    modal.modal('show');
  });

  /* remove error messages when modal closes */
  $('.modal').on('hidden.bs.modal', function () {
    $('.error').remove();
  });

  /* hide messages after 5 seconds */
  $('.footer .alert').delay(5000).fadeOut('slow');
});
