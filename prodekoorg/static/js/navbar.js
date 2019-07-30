$(document).ready(function() {
  var hamburger = $('.hamburger');
  hamburger.on('click', function() {
    hamburger.toggleClass('is-active');
  });
});
