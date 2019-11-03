$(document).ready(function() {
  $('#content').on('click', function() {
    if (
      $(window).width() < 992 &&
      !$('.navbar-toggler').hasClass('collapsed')
    ) {
      $('.navbar-toggler').trigger('click');
    }
  });

  function toggleNavbar() {
    if ($(window).width() >= 992) {
      if ($(this).scrollTop() > 50 || $(document).scrollTop() > 50) {
        $('#abit-navbar').css('opacity', '0.95');
        $('#scrollToTop').css('opacity', '1');
      } else {
        if ($(window).width() >= 992) $('#abit-navbar').css('opacity', '0');
        if ($(window).width() >= 992) $('#abit-navbar').css('display', 'none');
        $('#scrollToTop').css('opacity', '0');
      }
    } else {
      $('#abit-navbar').css('opacity', '0.95');
    }
  }

  toggleNavbar();

  // Create navbar background when scrolled
  $(document).scroll(function() {
    toggleNavbar();
  });

  // When header is clicked, scroll to top
  $('#scrollToTop').on('click', function(event) {
    event.preventDefault();
    $('html, body').animate(
      {
        scrollTop: 0
      },
      800,
      function() {}
    );
  });

  // Select all anchor links
  $(document).on('click', "a[href*='#']", function(event) {
    if (
      location.pathname.replace(/^\//, '') ==
        this.pathname.replace(/^\//, '') &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        event.preventDefault();
        $('html, body').animate(
          {
            scrollTop: target.offset().top - 130
          },
          600,
          function() {}
        );
      }
    }
  });
});
