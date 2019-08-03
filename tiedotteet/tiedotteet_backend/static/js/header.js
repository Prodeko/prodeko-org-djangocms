/* Update header based on scroll position */
$(document).ready(function() {
  $(window).scroll(function() {
    var pagetitle = 'Prodeko tiedotteet';
    var document_position = $(window).scrollTop();
    var dividers = document.getElementsByClassName('category-divider');
    for (var i = 0; i < dividers.length; i++) {
      var position = $(dividers[i]).offset().top;
      if (document_position >= position) {
        $('.navbar-brand').html($(dividers[i]).attr('category'));
      }
      if (document_position < 15) {
        $('.navbar-brand').html(pagetitle);
      }
    }
  });
});
