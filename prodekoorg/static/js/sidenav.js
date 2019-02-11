$(document).scroll(function() {
  checkOffset();
});

function checkOffset() {
  if (
    $('#sidenav').offset().top + $('#sidenav').height() >=
    $('#footer').offset().top - 10
  )
    $('#sidenav').css('position', 'absolute');
  if ($(document).scrollTop() + window.innerHeight < $('#footer').offset().top)
    $('#sidenav').css('position', 'fixed'); // restore when you scroll up
}
