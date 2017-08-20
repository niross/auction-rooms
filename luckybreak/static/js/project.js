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

  // Validate any forms on the page
  // $('form').each(function(i, form) {
  //   $($(form).serializeArray()).each(function(j, field) {
  //     validate_field($(form).find('[name="' + field.name + '"]'));
  //   });
  // });

  // Turn logout get requests into post requests
  $('.logout-link').click(function(e) {
    e.preventDefault();
    $(this).find('form').submit();
  });

});
