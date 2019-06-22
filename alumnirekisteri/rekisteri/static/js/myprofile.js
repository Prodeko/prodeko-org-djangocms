
$(document).ready(function(){
  /* get profile image data */
  imageData = {data:null};
  SimpleCrop($("#crop")[0], {
      confirmButton: $("#crop-save-image")[0],
      outputImage: $("#crop-image")[0],
      outputData: imageData,
      outputWidth: 1024,
      width: 512,
      height: 512
  });

  /* Submit main-form */
  $("#main-form").on("submit", function(event){
    event.preventDefault();
    $(".error").remove();
    var form = $(this);
    var formData = new FormData(form[0]);
    formData.append("crop_image_data", imageData.data);
    var request = $.ajax({
        url: form.attr("action"),
        data: formData,
        type: 'POST',
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response){
          if (response.success) {
            location.reload();
          } else {

            for (var key in response.errors.user_form){
              var errorElement = '<div class="error alert alert-danger">'+response.errors.user_form[key]+'</div>'
              $('input[name=user_form-'+key+']').after(errorElement);
            }
            for (var key in response.errors.person_form){
              var errorElement = '<div class="error alert alert-danger">'+response.errors.person_form[key]+'</div>'
              $('input[name=person_form-'+key+']').after(errorElement);
            }

          }
        }
    });
    return false;
  });

  /* All forms that are inside a modal with class modal-form
    will be submitted by this function. */
  $(".modal-form").on("submit", "form", function(event){
    event.preventDefault();
    $(".error").remove();
    var response = submitForm($(this).id, $(this).attr("action"), $(this).serialize());
    if (response.success) {
      location.reload();
    } else {
      for (var key in response.errors) {
        var errorElement = '<div class="error alert alert-danger">'+response.errors[key]+'</div>'
        $('input[name='+key+']').after(errorElement);
        $('select[name='+key+']').after(errorElement);
      }
    };
    return false;
  });

  /* get edit modal contents */
  $(".edit-link").on("click", function(event){
    event.preventDefault();
    var modal = $($(this).attr("modal"));
    var url = $(this).attr("url")
    $.get( url, function( data ) {
      modal.find(".modal-content").html( data );
    });
    modal.modal("show");
  });

  /* get delete modal contents */
  $(".delete-link").on("click", function(event){
    event.preventDefault();
    var modal = $($(this).attr("modal"));
    var url = $(this).attr("url")
    $.get( url, function( data ) {
      modal.find(".modal-content").html( data );
    });
    modal.modal("show");
  });

  updateVisibility = function(event){
      $(".panel:has(.category-checkbox:not(checked))").addClass("category-disabled");
      $(".panel:has(.category-checkbox:not(checked))").removeClass("category-enabled");
      $(".panel:has(.category-checkbox:checked)").removeClass("category-disabled");
      $(".panel:has(.category-checkbox:checked)").addClass("category-enabled");
  }
  $(".category-checkbox").on("change", updateVisibility);

  updateVisibility();
});


/* submit the form, having the given formId as id attribute,
    without reloading the page */
function submitForm(formId, url, data){
  var form = document.getElementById(formId);
  var responseText;
  var jqXHR = $.ajax({
    type: "POST",
    url: url,
    data: data,
    dataType: "json",
    async: false
  });
  return jqXHR.responseJSON;
}

/* remove error messages when modal closes */
$('.modal').on('hidden.bs.modal', function () {
    $(".error").remove();
})

/* hide messages after 5 seconds */
$(".footer .alert").delay(5000).fadeOut('slow');