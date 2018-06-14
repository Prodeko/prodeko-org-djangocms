function updateTexts(virka) {
  $('#vaalitKysymysForm small').html(virka + ' - Esitä kysymys');
  $('#header').html(virka);
  // Set hidden input field
  $('.input-virka').attr('value', virka);
}

selectedTab_id = localStorage.getItem('selectedTab_id');
selectedVirka = localStorage.getItem('selectedVirka');

$(document).ready(function() {

  /* START stay on same navigation tab with reload */
  var elem;
  var virka;

  /* Use localStorage to display the tab that was open
  *  before the latest refresh.
  */
  if ($('#vaalitNav').length > 0) {
    if (selectedTab_id != null) {
      elem = $('.list-group-root a[data-toggle="tab"][href="' + selectedTab_id + '"]');

      virka = elem.text().trim();
      updateTexts(virka);
      checkBtnHaeVirkaanVisibility(virka);  // Defined in 'vaalit_question_form.html'

      elem.addClass('.active');
      elem.tab('show');
    } else {
      // No tab saved in localStorage
      elem = $('.list-group-root a[data-toggle="tab"][href="#_1"]');

      virka = elem.text().trim();
      checkBtnHaeVirkaanVisibility(virka);
      updateTexts(virka);

      elem.addClass('.active');
      elem.tab('show');
    }
  }



  $('.list-group-root a[data-toggle="tab"]').click(function (e) {
      var id = $(e.delegateTarget).attr("href");
      var virka = $('.list-group-root a[data-toggle="tab"][href="' + id + '"]').text().trim();
      checkBtnHaeVirkaanVisibility(virka);

      localStorage.setItem('selectedTab_id', id);
      localStorage.setItem('selectedVirka', virka);

      updateTexts(virka);

      var listType = $(e.delegateTarget).closest('div').attr('id');
      if (listType == 'hallitusList') {
        $('#toimaritList > a.active').removeClass('active');
      } else if (listType == 'toimaritList') {
        $('#hallitusList > a.active').removeClass('active');
      }
  });
  /* END stay on same navigation tab with reload */

  /* Ehdokas object delete confirmation in modal */
  $(".showDeleteEhdokasModal").click(function(e) {
    e.preventDefault();
    var ehdokasId = $(e.target).attr('ehdokas-id');
    $('#formDeleteEhdokas').attr('action', '/vaalit/delete-ehdokas/' + ehdokasId + '/');
    $('#confirmDeleteEhdokasModal').modal('toggle');
  });

  /* Display answer form */
  $('#btnVastaaKysymykseen').click(function () {
    $('#vaalitWrapperAnswerForm').toggle();
  });

  /* Display apply form */
  $('#btnHaeVirkaan').click(function () {
    $('#btnHaeVirkaan').toggleClass('animate-chevron');
    $('#vaaliWrapperApplyForm').slideToggle();
  });


  /* Ehdokas picture cropping */
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
      $('.crop-preview').height('100px');
      $('.crop-preview').attr('src', cropDataURL);
      $('#modalCrop').modal('hide');
    });
  });
});
