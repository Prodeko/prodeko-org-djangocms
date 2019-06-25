$(document).scroll(function() {
  //checkOffset(); # Uncomment and update css files to enable scrolling sidenav
});

function checkOffset() {
  if (
    $('#sidenav').offset().top + $('#sidenav').height() >=
    $('#footer').offset().top - 100
  ) {
    $('#sidenav').css('position', 'absolute');
    $('#sidenav').css('bottom', '0px');
  }
  if (
    $(document).scrollTop() + window.innerHeight <
    $('#footer').offset().top
  ) {
    $('#sidenav').css('position', 'fixed'); // restore when you scroll up
    $('#sidenav').css('bottom', '40px');
  }
}
