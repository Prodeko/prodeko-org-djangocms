$(document).ready(function () {
  $('h2').fitText(1.2, { maxFontSize: '45px' })
  $('h3').fitText(1, { maxFontSize: '36px' })
  $('h1').fitText(0.9, { maxFontSize: '60px' })

  $('#content').on('click', function () {
    if ($(window).width() < 800 && $('#content').hasClass('blur')) { $('.navbar-toggle').trigger('click') }
  })

  // Creates blur effect in the background when the menu icon is clicked on mobile
  $('.navbar-toggle').on('click', function () {
    if ($('#content').hasClass('blur')) {
      $('#content').removeClass('blur')
    } else {
      $('#content').addClass('blur')
    }
  })

  // Setup by device and scroll: if start position is not on top, create background for navbar
  if ($(window).width() < 800) $('#myNavbar').css('opacity', '1')
  if ($(window).scrollTop() > 50) {
    $('#navbar').css('background-position', 'left 0px')
    $('#scrollToTop').css('opacity', '1')
    $('#myNavbar').css('opacity', '1')
  }

  // Create navbar background when scrolled
  $(window).scroll(function () {
    if ($(this).scrollTop() > 50 || $(document).scrollTop() > 50) {
      $('#navbar').css('background-position', 'left 0px')
      $('#myNavbar').css('opacity', '1')
      $('#scrollToTop').css('opacity', '1')
    } else {
      $('#navbar').css('background-position', 'left -300px')
      if ($(window).width() > 800) $('#myNavbar').css('opacity', '0')
      $('#scrollToTop').css('opacity', '0')
    }
  })

  // When header is clicked, scroll to top
  $('#scrollToTop, #logo').on('click', function (event) {
    event.preventDefault()
    $('html, body').animate(
      {
        scrollTop: 0
      },
      800,
      function () {}
    )
  })

  // Select all links with hashes
  $(document).on('click', "a[href*='#']", function (event) {
    if ($(window).width() < 800 && $('#content').hasClass('blur')) { $('.navbar-toggle').trigger('click') }
    if (
      location.pathname.replace(/^\//, '') ==
        this.pathname.replace(/^\//, '') &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash)
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']')
      if (target.length) {
        event.preventDefault()
        $('html, body').animate(
          {
            scrollTop: target.offset().top - 100
          },
          1000,
          function () {}
        )
      }
    }
  })
})
