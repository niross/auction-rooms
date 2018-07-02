/* eslint-disable */
$(function() {
  var target = document.getElementById('map');
  var center = new google.maps.LatLng(
    parseFloat(target.dataset.latitude),
    parseFloat(target.dataset.longitude)
  );
  var map = new google.maps.Map(target, {
    zoom: 16,
    center: center,
    mapTypeId: 'roadmap'
  });

  new google.maps.Circle({
    strokeColor: '#26a69a',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#26a69a',
    fillOpacity: 0.35,
    map: map,
    center: center,
    radius: 100
  });
});
