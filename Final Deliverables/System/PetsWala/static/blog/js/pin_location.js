let position = null;
let lat = null;
let lng = null;
let marker = null;
let toogle = false;
let toogleOption = document.getElementById("toggleOptionsHtml");

function showPosition(pos) {
  position = pos;
  initMap()
}

function toogleInput() {
  const cb = document.getElementById('option1');
  const cb2 = document.getElementById('option2')

  if (cb.checked) {
    toogleOption.innerHTML = `
    <input id="searchTextField" class="form-control my-3" type="text" size="50">
    `
    placeSearchBox()
  }
  else if (cb2.checked) {
    toogleOption.innerHTML = `
    <div id="Adreess_option"></div>
    <p>Select Pin Location from Map.</p>
    <p id="writeAddressDiv"></p>
    <div id="map"></div>
    `
    initMap()
  }
}

function initMap() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(showPosition, showError);
  }

  if (position) {
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    const uluru = { lat: lat, lng: lng };
    let el = document.getElementById("map");
    if (el) {
      const map = new google.maps.Map(el, {
        zoom: 13,
        center: uluru,
      });
      marker = new google.maps.Marker({
        position: uluru,
        map: map,
        draggable: true,
        title: "select location"
      });

      marker.addListener("dragend", (event) => {
        lat = event.latLng.lat();
        lng = event.latLng.lng();
        geocodeLatLng();
      });
      geocodeLatLng();
    }

  }
}

function geocodeLatLng() {
  const latlng = {
    lat: lat,
    lng: lng,
  };

  if (!lat && !lng) {
    address.innerHTML = "<p>Address: Location Unaccessible</p>"
  } else {
    let address = document.getElementById("writeAddressDiv");
    if (address) {
      const geocoder = new google.maps.Geocoder();
      geocoder
        .geocode({ location: latlng })
        .then((response) => {
          if (response.results[0]) {
            setHiddenValues(response.results[0].formatted_address, lat, lng);
            address.innerHTML = "<p>Address: " + response.results[0].formatted_address + "</p>"
          } else {
            address.innerHTML = "<p>Address: Unknow address</p>"
          }
        })
        .catch((e) => window.alert("Geocoder failed due to: " + e));
    }

  }
}

function showError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      break;
  }
}

function placeSearchBox() {

  let defaultBounds = null;
  if (lat && lng) {
    const center = { lat: lat, lng: lng };
    // Create a bounding box with sides ~10km away from the center point
    defaultBounds = {
      north: center.lat + 0.1,
      south: center.lat - 0.1,
      east: center.lng + 0.1,
      west: center.lng - 0.1,
    };
  }

  let options = null;
  if (defaultBounds) {
    options = {
      bounds: defaultBounds,
      componentRestrictions: { country: "pk" },
      fields: ["address_components", "geometry", "icon", "name"],
      strictBounds: false,
      types: ["establishment"],
    };
  } else {
    options = {
      componentRestrictions: { country: "pk" },
      fields: ["address_components", "geometry", "icon", "name"],
      strictBounds: false,
      types: ["establishment"],
    };
  }
  var input = document.getElementById('searchTextField');
  let autocomplete = new google.maps.places.Autocomplete(input, options);

  google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var place = autocomplete.getPlace();
    lat = place.geometry.location.lat();
    lng = place.geometry.location.lng();
    setHiddenValues(place.name, place.geometry.location.lat(), place.geometry.location.lng());
  });
}

function setHiddenValues(address, lat, lng) {
  document.getElementById('addresss').value = address;
  document.getElementById('lat').value = lat;
  document.getElementById('lng').value = lng;
}

function handleSubmission(event) {
  let a = document.getElementById('addresss').value;
  let l1 = document.getElementById('lat').value;
  let l2 = document.getElementById('lng').value;

  if (!a || !l1 || !l2) {
    alert("Please select an address");
    event.preventDefault();
  }
}