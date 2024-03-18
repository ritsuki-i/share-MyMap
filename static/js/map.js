function loadGoogleMapsAPI() {
  let script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${mapParams.googleMapKey}&v=weekly`;
  document.head.appendChild(script);
  script.onload = () => {
    initMap(mapParams.lat, mapParams.lng, mapParams.zoom);
  };
}

function initMap(lat, lng, zoom) {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: zoom,
    center: {lat: mapParams.lat, lng: mapParams.lng},
  });

  if (mapParams.mapMarker && mapParams.mapMarker.lat && mapParams.mapMarker.lng) {
    let marker = new google.maps.Marker({
      position: {lat: parseFloat(mapParams.mapMarker.lat), lng: parseFloat(mapParams.mapMarker.lng)},
      map,
      title: mapParams.mapMarker.title ? mapParams.mapMarker.title : 'No Title',
    });

    marker.addListener('click', () => {
      infoWindow.setContent(mapParams.mapMarker.description ? mapParams.mapMarker.description : 'No Description');
      infoWindow.open(map, marker);
    });
  }

  let infoWindow = new google.maps.InfoWindow();

  map.addListener("click", (mapsMouseEvent) => {
    if (infoWindow) infoWindow.close();

    const latLng = mapsMouseEvent.latLng.toJSON();
    infoWindow = new google.maps.InfoWindow({
      position: latLng,
    });

    infoWindow.setContent(
      `<form action="/" method="post">
        <input type="hidden" name="form_type" value="submit_location">
        <input type="hidden" id="lat" name="lat" value="${latLng.lat}">
        <input type="hidden" id="lng" name="lng" value="${latLng.lng}">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br>
        <label for="description">Description:</label>
        <input type="text" id="description" name="description"><br>
        <input type="submit" value="Submit">
      </form>`
    );

    infoWindow.open(map);
  });
}

loadGoogleMapsAPI();