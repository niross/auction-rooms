/* eslint-disable */
$(document).ready(function() {

  // Add csrf token to ajax requests
  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        var csrftoken = Cookies.get('csrftoken');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });

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

  // Initialise modals
  $('.modal').modal();

  // Initialise location autocompletes
  if ($('.location-autocomplete').length > 0) {
    var autocomplete = new google.maps.places.Autocomplete(
      $('.location-autocomplete').get(0), {
        types: ['geocode']
      }
    );
    autocomplete.addListener('place_changed', function () {
      var place = autocomplete.getPlace();
      $('.location-autocomplete-coords').val(
        place.geometry.location.lat()
        + ',' +
        place.geometry.location.lng()
      );
    });
  }

  // Show the search nav after the page has loaded
  $('.search-nav').fadeIn();

  // Favourite auctions add/remove
  $('.auction-favourite').click(function(e) {
    var el = $(this);
    if ($(el).attr('data-authenticated')) {
      e.stopPropagation();
      if ($(el).attr('data-favourite')) {
        $.ajax({
          url: '/api/auctions/favourites/' + $(el).attr('data-auction-id') + '/',
          type: 'DELETE',
          success: function () {
            $(el).removeAttr('data-favourite', true);
            $(el).attr('data-tooltip', 'Add to your favourites');
            $(el).tooltip({ delay: 50, html: true, position: 'top' });
            $(el).find('.material-icons').text('favorite')
          }
        })
      }
      else {
        $.post(
          '/api/auctions/favourites/',
          { auction: $(el).attr('data-auction-id') },
          function() {
            $(el).attr('data-favourite', true);
            $(el).attr('data-tooltip', 'Remove from your favourites');
            $(el).tooltip({ delay: 50, html: true, position: 'top' });
            $(el).find('.material-icons').text('check');
          }
        )
      }
    }
  });
});
