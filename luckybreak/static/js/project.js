/* eslint-disable */
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
    closeOnSelect: true
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
  $('.tooltipped').tooltip({ delay: 50, html: true, position: 'top' });

  // Initialise time pickers
  $('.timepicker').pickatime({
    twelvehour: false
  });

  // Initialise feature discovery
  $('.tap-target').tapTarget('open');

  // Initialise location autocompletes
  var autocomplete = new google.maps.places.Autocomplete(
    $('.location-autocomplete').get(0), {
      types: ['geocode']
    }
  );
  autocomplete.addListener('place_changed', function() {
    var place = autocomplete.getPlace();
    $('.location-autocomplete-coords').val(
      place.geometry.location.lat()
      + ',' +
      place.geometry.location.lng()
    );
  });

  $('.search-results .search-nav').fadeIn();
});
