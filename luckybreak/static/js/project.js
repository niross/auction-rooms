$(document).ready(function() {
  // Initialise all select inputs on the page
  $('select').material_select();

  // Initialise material datepicker
  $('.datepicker').pickadate({
    selectMonths: true,
    selectYears: 15,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: false
  });

  // Initialise side nav for mobile
  $('.button-collapse').sideNav();

  // Turn logout get requests into post requests
  $('.logout-link').click(function(e) {
    e.preventDefault();
    $(this).find('form').submit();
  });

	// Initialise collapsibles
  $('.collapsible').collapsible();

  // Initialise tooltips
  $('.tooltipped').tooltip({delay: 50});
});
