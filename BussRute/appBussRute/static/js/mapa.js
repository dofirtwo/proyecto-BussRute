var map = L.map('map').setView([2.9341049606236704, -75.28170112926662], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

document.getElementById('site-select').addEventListener('change', function() {
    var site = this.value;
    removeRoute();
    updateRoute(site);
});

var control;

function removeRoute() {
    if (control){
        control.remove();
    }
}

function updateRoute(site) {
  var options = {
    lineOptions: {
      styles: [{ color: 'black', weight: 6 }]
    },
    addWaypoints: false,
    createMarker: function() { return null; },
    draggableWaypoints: false,
    fitSelectedRoutes: 'smart',
    showAlternatives: false
  };

  control = L.Routing.control(options).addTo(map);

    switch (site) {
        case 'Ruta7':
            control.setWaypoints([
                L.latLng(2.922685, -75.285125),
                L.latLng(2.937675, -75.289153),
                L.latLng(2.940343, -75.282133),
                L.latLng(2.944742, -75.288868),
                L.latLng(2.962675, -75.287648),
                L.latLng(2.944742, -75.288868),
                L.latLng(2.940343, -75.282133),
                L.latLng(2.937675, -75.289153),
                L.latLng(2.922685, -75.285125),
            ]);
            break;
        case 'Ruta19':
            control.setWaypoints([
                L.latLng(2.913977, -75.280796),
                L.latLng(2.915499, -75.282797),
                L.latLng(2.962675, -75.287648)
            ]);
            break;
        case 'London':
            break;
        default:
            return;
    }


    control.hide();
}