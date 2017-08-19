/**
 * Location typeahead.
 *
 * Every location input needs an associated latitude and longitude field.
 *
 * If a valid location is selected the location, latitude and longitude fields
 * should be updated with new values.
 *
 * If an invalid location is entered (on blur no selection was made and the
 * location input contains text) remove any lat/lng values and show
 * an error.
 *
 * If no location is entered (on blur location input value == '') clear
 * errors and lat/lng values.
 *
 * @param afterSelectCallback
 */
/* eslint-disable */

(function ( $ ) {
  $.fn.locationTypeahead2 = function (options) {
    return this.each(function() {
      var locationEl = $(this);
      var settings = $.extend({
        latitudeField: $(locationEl).parents('.form-group').find('[name="latitude"]'),
        longitudeField: $(locationEl).parents('.form-group').find('[name="longitude"]'),
        errorIcon: false,
        initialLocation: {
          location: null,
          latitude: null,
          longitude: null
        }
      }, options);


      var autocomplete = new google.maps.places.Autocomplete($(locationEl).get(0));
      autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        $(settings.latitudeField).val(place.geometry.location.lat());
        $(settings.longitudeField).val(place.geometry.location.lng());
      });

      $(locationEl).on('input', function(e) {
        $(settings.latitudeField).val('');
        $(settings.longitudeField).val('');
      });

      function clearErrors() {
        var fg = $(locationEl).parents('.form-group');
        $(fg).removeClass('has-error').removeClass('has-feedback');
        $(fg).find('.form-control-feedback').remove();
        $(fg).find('.help-text').remove();
      }

      function showError() {
        var fg = $(locationEl).parents('.form-group');
        $(fg)
          .addClass('has-error')
          .append('<div class="help-text">Please select a valid location</div>');
        if (settings.errorIcon) {
          $(fg)
            .addClass('has-feedback')
            .append('<span class="fa fa-exclamation-circle form-control-feedback"></span>')
        }
      }

    });
  }
}(jQuery));
