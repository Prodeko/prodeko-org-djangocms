$(document).ready(function() {
  console.log(window.location.href);
  $('#policy-modal').on('hide.bs.modal', function(e) {
    e.preventDefault();
  });

  const currentPage = window.location.href;
  if (
    !currentPage.endsWith('/tietosuoja/') &&
    !currentPage.endsWith('/privacy-policy/')
  ) {
    $('#policy-modal').modal('show');
  }
});
