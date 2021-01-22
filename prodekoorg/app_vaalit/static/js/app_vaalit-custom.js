function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function updateTexts(virka) {
  if (!virka) {
    return;
  }
  $("#vaalitKysymysForm small").html(virka + " - Esitä kysymys");
  updateDescription(virka) // Defined in vaalit_content.html
  $("#header").html(virka);
  // Set hidden input field
  $(".input-virka").val(virka);
}


var selectedTab_id = localStorage.getItem("selectedTab_id");
var selectedVirka = localStorage.getItem("selectedVirka");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(document).ready(function() {
  /* START stay on same navigation tab with reload */
  var elem;
  var virka;
  //$('#electionsContent').addClass('hidden');

  /* Use localStorage to display the tab that was open
   *  before the latest refresh.
   */
  if ($("#vaalitNav").length > 0) {
    if (selectedTab_id != null && selectedTab_id != "null") {
      elem = $(
        '.list-group-root a[data-bs-toggle="tab"][href="' + selectedTab_id + '"] .virka-name'
      );
      elem2 = $(selectedTab_id);
      elem2.addClass("active show");
      
      $('#electionsContent').removeClass('hidden');
      $('#landingpageContent').addClass('hidden');

      $('#q_' + selectedTab_id.slice(2)).addClass("active show");

      virka = elem.text().trim();
      updateTexts(virka);
      checkBtnHaeVirkaanVisibility(virka); // Defined in 'vaalit_question_form.html'
      
      markRead(selectedTab_id.slice(2));      // Mark viewed "virka" as read

      elem.addClass("active show");
      elem.tab("show");
    } else {
      // No tab saved in localStorage
       //$('#electionsContent').addClass('hidden');
       openFrontPage();
    }
  }

  function openFrontPage() {
    $("#toimaritList > a.active").removeClass("active");
    $("#hallitusList > a.active").removeClass("active");
    $('#electionsContent').addClass('hidden');
    $('#landingpageContent').removeClass('hidden');
    var previousId = localStorage.getItem("selectedTab_id")
    if (previousId != null) {
      $('#q_' + previousId.slice(2)).removeClass("active show");
    }

    localStorage.setItem("selectedTab_id", null);
    localStorage.setItem("selectedVirka", null);

    document.getElementById("landingPageTitle").scrollIntoView({behavior: "smooth", block: "start"});
  }

  $('.vaalitFrontpageLink').click(function(e) {
    e.preventDefault();
    openFrontPage();
  })

  $('.list-group-root a[data-bs-toggle="tab"]').click(function(e) {
    var id = $(e.delegateTarget).attr("href");
    var virka = $('.list-group-root a[data-bs-toggle="tab"][href="' + id + '"] .virka-name')
      .text()
      .trim();
    checkBtnHaeVirkaanVisibility(virka);

    var previousId = localStorage.getItem("selectedTab_id")
    if (previousId != null) {
      $('#q_' + previousId.slice(2)).removeClass("active show");
    }

    document.getElementById("header").scrollIntoView({behavior: "smooth", block: "start"});

    localStorage.setItem("selectedTab_id", id);
    localStorage.setItem("selectedVirka", virka);

    $('#electionsContent').removeClass('hidden');
    $('#landingpageContent').addClass('hidden');

    $('#q_' + id.slice(2)).addClass("active show");

    updateTexts(virka);
    $("#vaaliApplyForm").hide(); // Hide "apply to virka form" when changing tabs if it's open
    markRead(id.slice(2));      // Mark viewed "virka" as read

    var listType = $(e.delegateTarget)
      .closest("div")
      .attr("id");
    if (listType == "hallitusList") {
      $("#toimaritList > a.active").removeClass("active");
    } else if (listType == "toimaritList") {
      $("#hallitusList > a.active").removeClass("active");
    }
  });
  /* END stay on same navigation tab with reload */

  /* Ehdokas object delete confirmation in modal */
  $(".showDeleteEhdokasModal").click(function(e) {
    e.preventDefault();
    var ehdokasId = $(e.target).attr("ehdokas-id");
    $("#formDeleteEhdokas").attr(
      "action",
      "delete-nominee/" + ehdokasId + "/"
    );
    $("#confirmDeleteEhdokasModal").modal("toggle");
  });

  /* Display apply form */
  $("#btnHaeVirkaan").click(function() {
    $("#btnHaeVirkaan").toggleClass("animate-chevron");
    $("#vaaliApplyForm").slideToggle();
  });

  /* AJAX creation of kysymys objects */
  $("#vaalitKysymysForm").submit(function(e) {
    e.preventDefault();
    var formData = $(this).serialize();
    $.ajax({
      url: "",
      type: "POST",
      // Add 'submitKysymys' to the POST data
      // to have correct handling in the views.py main view
      data: formData + "&submitKysymys=",
      success: createKysymysSuccess,
      error: createKysymysError
    });
  });

  function createKysymysSuccess(data, textStatus, jqXHR) {
    $("#vaaliContent .tab-pane.active .vaalitKysymysList").prepend(data);
    $("#vaaliContent .tab-pane.active .vaalitDeleteKysymysForm button")
      .first()
      .click(ajaxDeleteKysymys);
    $("[name='question']").val('');
  }

  function createKysymysError(jqXHR, textStatus, errorThrown) {
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
  }

  /* AJAX deletion of Kysymys objects */
  $(".vaalitDeleteKysymysForm button").click(ajaxDeleteKysymys);

  function ajaxDeleteKysymys(e) {
    e.preventDefault();
    $(this).prop("disabled", true); // Disallow the button so it can't be clicked twice
    var formData = $(this)
      .parent()
      .serialize();
    var kysymysId = $(this)
      .siblings("input[name=hidden-kysymys-id]")
      .val();

    $.ajax({
      url: "delete-question/" + kysymysId + "/",
      type: "POST",
      // Add 'submitKysymys' to the POST data
      // to have correct handling in the views.py main view
      data: formData,
      success: deleteKysymysSuccess,
      error: deleteKysymysError
    });
  }

  function deleteKysymysSuccess(data, textStatus, jqXHR) {
    $("#kysymys_" + data.delete_kysymys_id).fadeOut(300, function() {
      $(this).remove();
    });
    $("#vastaukset_" + data.delete_kysymys_id).fadeOut(300, function() {
      $(this).remove();
    });
  }

  function deleteKysymysError(jqXHR, textStatus, errorThrown) {
    console.log("err")
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
  }

  function markRead(virka_id) {
    $.ajax({
      url: "mark-read/" + virka_id + "/",
      type: "POST",
      success: markReadSuccess(virka_id),
      error: markReadError
    });
  }

  function markReadSuccess(virka_id) {
    $('.list-group-root a[data-bs-toggle="tab"][href="' + "#_" + virka_id + '"] .virka-unread').fadeOut(200, function() {
      $(this).remove();
    })
  }

  function markReadError(jqXHR, textStatus, errorThrown) {
    console.log("err")
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
  }

  /* Ehdokas picture cropping */
  $(function() {
    /* Open cropper modal with preview */
    $("#id_pic").change(function() {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $("#modalCrop #image").attr("src", e.target.result);
          $("#modalCrop").modal("show");
        };
        reader.readAsDataURL(this.files[0]);
      }
    });

    /* Create the cropper and handle zooming, closing and displaying a preview */
    var $image = $("#modalCrop #image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop")
      .on("shown.bs.modal", function() {
        $image.cropper({
          viewMode: 2,
          aspectRatio: 1 / 1,
          minCropBoxWidth: 100,
          minCropBoxHeight: 100,
          ready: function() {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
          }
        });
      })
      .on("hidden.bs.modal", function() {
        // Destroy previous cropper on modal hide
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
      });

    $("#modalCrop .js-zoom-in").click(function() {
      $image.cropper("zoom", 0.1);
    });

    $("#modalCrop .js-zoom-out").click(function() {
      $image.cropper("zoom", -0.1);
    });

    /* Handle cropped modal data */
    $("#modalCrop .js-crop-and-upload").click(function() {
      var cropData = $image.cropper("getData");
      var cropDataURL = $image.cropper("getCroppedCanvas").toDataURL();
      $("#x").val(cropData.x);
      $("#y").val(cropData.y);
      $("#h").val(cropData.height);
      $("#w").val(cropData.width);
      $(".crop-preview").height("100px");
      $(".crop-preview").attr("src", cropDataURL);
      $("#modalCrop").modal("hide");
    });
  });
});
