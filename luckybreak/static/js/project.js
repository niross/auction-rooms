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
});
