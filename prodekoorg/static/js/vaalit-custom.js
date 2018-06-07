$(document).ready(function() {

  $('.list-group-root div.list-group > a').on('click', function(e) {
    // Handle updating the header text, trim is needed
    var virka = $(e.target).first().text().trim();
    $('#vaalitKysymysForm small').html(virka + ' - Esitä kysymys');
    $('#header').html(virka);
    // Set hidden input field
    $('.input-virka').attr('value', virka);

    // Handle nested list group deactivation
    var listType = $(e.delegateTarget).closest('div').attr('id');
    if (listType == 'hallitusList') {
      $('#toimaritList > a.active').removeClass('active');
    } else if (listType == 'toimaritList') {
      $('#hallitusList > a.active').removeClass('active');
    }
  });

  $('#btnVastaaKysymykseen').click(function () {
    $('#vaalitWrapperAnswerForm').toggle();
  });

  $(function() {

    /* Open cropper modal with preview */
    $("#id_pic").change(function() {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $("#image").attr("src", e.target.result);
          $("#modalCrop").modal("show");
        };
        reader.readAsDataURL(this.files[0]);
      }
    });

    /* Create the cropper and handle zooming, closing and displaying a preview */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function() {
      $image.cropper({
        viewMode: 2,
        aspectRatio: 1 / 1,
        minCropBoxWidth: 100,
        minCropBoxHeight: 100,
        ready: function() {
          $image.cropper("setCanvasData", canvasData);
          $image.cropper("setCropBoxData", cropBoxData);
        },
      });
    }).on("hidden.bs.modal", function() {
      // Destroy previous cropper on modal hide
      cropBoxData = $image.cropper("getCropBoxData");
      canvasData = $image.cropper("getCanvasData");
      $image.cropper("destroy");
    });

    $(".js-zoom-in").click(function() {
      $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function() {
      $image.cropper("zoom", -0.1);
    });

    /* Handle cropped modal data */
    $(".js-crop-and-upload").click(function() {
      var cropData = $image.cropper("getData");
      var cropDataURL = $image.cropper('getCroppedCanvas').toDataURL();
      $("#x").val(cropData.x);
      $("#y").val(cropData.y);
      $("#h").val(cropData.height);
      $("#w").val(cropData.width);
      $('#crop-preview').height('100px');
      $('#crop-preview').attr('src', cropDataURL);
      $('#modalCrop').modal('hide');
    });
  });
});
