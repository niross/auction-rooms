/* eslint-disable */
$(function() {
  $('.guest-confirmation-modal .print').click(function() {
    $(this).parents('.modal').find('.printme').print();
  });

  // Open a modal if id provided
  if (window.location.hash && window.location.hash !== '#!' && $(window.location.hash)) {
    var el = $(window.location.hash);
    if ($(el).hasClass('modal')) {
      $(el).modal('open');
    }
  }
});
