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
});

// eslint-disable-next-line no-unused-vars
function post(user_id) {
  const is_liked = $('#like_button').hasClass('fas');
  $.ajax({
    url: 'like/' + user_id + '/',
    type: 'POST',
    data: { is_liked: is_liked },
    success: function (data) {
      $('.total-likes').text(data['total_likes']);
      if (is_liked) {
        $('#like_button').removeClass().addClass('far fa-heart');
      } else {
        $('#like_button').removeClass().addClass('fas fa-heart');
      }
    },
  });
}
