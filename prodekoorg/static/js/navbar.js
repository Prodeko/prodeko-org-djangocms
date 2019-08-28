$(document).ready(function() {
  var hamburger = $('.hamburger');

  function preventScrolling() {
    $('body').css('overflow', 'hidden');
    $('body').css('position', 'fixed');
  }

  function allowScrolling() {
    $('body').css('overflow', 'visible');
    $('body').css('position', 'static');
  }

  hamburger.on('click', function() {
    hamburger.toggleClass('is-active');
    hamburger.hasClass('is-active') ? preventScrolling() : allowScrolling();
  });
});
