$(function() {
  $('input[name="location"]').locationTypeahead2({
    errorIcon: true,
    latitudeField: $('input[name="latitude"]'),
    longitudeField: $('input[name="longitude"]')
  });
});
