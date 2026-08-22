/* Get csrf_token */
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/* delete-user post */
function deleteUser(user_id) {
  var post_data = {
    csrfmiddlewaretoken: csrftoken,
    action: 'delete-user',
    user_id: user_id,
  };
  $.post('/admin/', post_data, function () {
    location.reload();
  });
}

/* delete user popup */
$('.delete-user-button').click(function () {
  var user_id = $(this).attr('user-id');
  var user_name = $(this).attr('user-name');
  $('#delete-user-modal').modal('show');
  $('#delete-user-modal #modal-user-name').html(user_name);
  $('#delete-user-modal #delete-user').attr('user-id', user_id);
});

/* confirm delete user */
$('#delete-user-modal #delete-user').click(function () {
  var user_id = $(this).attr('user-id');
  deleteUser(user_id);
  //location.reload();
});
