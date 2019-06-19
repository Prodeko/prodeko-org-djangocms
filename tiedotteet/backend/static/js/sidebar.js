$(document).ready(function() {

  var width = $(window).width();
  if (width >= 768){
    $(".container").addClass("open-sidebar");
    $("#sidebar").addClass("open");
    $(".swipe-area").addClass("open");
  }

  $("[data-toggle]").click(function() {
    var toggle_el = $(this).data("toggle");
    $(toggle_el).toggleClass("open-sidebar");
    $("#sidebar").toggleClass("open");
    $(".swipe-area").toggleClass("open");
  });

});

$(window).on("swipeleft",function(){
  $(".container").removeClass("open-sidebar");
  $("#sidebar").removeClass("open");
  $(".swipe-area").removeClass("open");
});

$(".swipe-area").on("swiperight",function(){
  $(".container").addClass("open-sidebar");
  $("#sidebar").addClass("open");
  $(".swipe-area").addClass("open");
});


$(window).resize(function() {
  var width = $(window).width();
  if (width >= 768){
    $(".container").addClass("open-sidebar");
    $("#sidebar").addClass("open");
    $(".swipe-area").addClass("open");
  } else {
    $(".container").removeClass("open-sidebar");
    $("#sidebar").removeClass("open");
    $(".swipe-area").removeClass("open");
  }
});
