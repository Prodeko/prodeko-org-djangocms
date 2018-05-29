$(document).ready(function() {

  $('.list-group-root div.list-group > a').on('click', function(e) {

    if(!$('#vaaliWrapperContent').is(':visible')) {
      // Handle pressing sidenav while "Hae virkaan" view is active
      $('#vaaliWrapperForm').fadeOut(300);
      $('#vaaliWrapperContent').delay(100).fadeIn(300);
    } else {
      // Handle updating the form text
      $('#vaalitKysymysForm').removeClass('d-none');
      $('#btnHaeVirkaan').removeClass('d-none');
      var virka = $(e.target).first().text();
      $('#vaalitKysymysForm small').html(virka + ' - Esitä kysymys');
      $('#header').html(virka);

      // Handle nested list group deactivation
      var listType = $(e.delegateTarget).closest('div').attr('id');
      if (listType == 'hallitusList') {
        $('#toimaritList > a.active').removeClass('active');
      } else if (listType == 'toimaritList') {
        $('#hallitusList > a.active').removeClass('active');
      }
    }
  });

  $('#btnHaeVirkaan').click(function () {
    $('#header').html("Hae virkaan");
    $('#vaaliWrapperForm').fadeIn(300);
    $('#vaaliWrapperContent').fadeOut(300);
  });

  $('#btnEtusivu').click(function () {
    // Get the current active sidenav selection. For example 'Puheenjohtaja', 'Mediakeisari' etc.
    const header = $('.list-group-root a.active > span:visible').html();
    $('#header').html(header);
    $('#vaaliWrapperContent').fadeIn(300);
    $('#vaaliWrapperForm').fadeOut(300);
  });


  $(function() {

    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_pic").change(function() {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $("#image").attr("src", e.target.result);
          $("#modalCrop").modal("show");
        }
        reader.readAsDataURL(this.files[0]);
      }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function() {
      $image.cropper({
        viewMode: 3,
        aspectRatio: 1 / 1,
        minCropBoxWidth: 100,
        minCropBoxHeight: 100,
        ready: function() {
          $image.cropper("setCanvasData", canvasData);
          $image.cropper("setCropBoxData", cropBoxData);
        },
      });
    }).on("hidden.bs.modal", function() {
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

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function() {
      var cropData = $image.cropper("getData");

      var cropDataURL = $image.cropper('getCroppedCanvas').toDataURL();
      $("#id_x").val(cropData.x);
      $("#id_y").val(cropData.y);
      $("#id_height").val(cropData.height);
      $("#id_width").val(cropData.width);
      var fu = $("#id_pic");
      fu.fileupload('option', 'url', cropDataURL);
      $("#formUpload").submit();
    });

  });
});
