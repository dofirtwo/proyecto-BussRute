let rutas =[]
let coodernadas =[]


var map = L.map('map').setView([2.9341049606236704, -75.28170112926662], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

document.getElementById('ruta').addEventListener('change', function() {
    var site = this.value;
    removeRoute();
    updateRoute(site);
    mostrarDatosTabla()
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
        styles: [{ color: '#00A99D' }]
    },
    addWaypoints: false,
    createMarker: function() { return null; },
    draggableWaypoints: false,
    fitSelectedRoutes: 'smart',
    showAlternatives: false
  };

  control = L.Routing.control(options).addTo(map);
   // Crear un arreglo para almacenar las coordenadas
  var waypoints = [];
  numeroRut = document.getElementById("ruta").value
  // Recorrer el arreglo de coordenadas y agregar cada punto al arreglo de waypoints
  coodernadas.forEach(entradaR => {
    posC = rutas.findIndex(ruta=>ruta.numRuta==entradaR.idRuta);
    if (rutas[posC].numRuta == numeroRut){
        if(rutas[posC].empRuta == "Coomotor"){
            document.getElementById("txtColor").value = "Azul"
            document.getElementById("txtImagen").src = '../../static/img/Coomotor.jpg'
        }
        if(rutas[posC].empRuta == "Cootranshuila"){
            document.getElementById("txtColor").value = "Verde Claro con Blanco"
            document.getElementById("txtImagen").src = '../../static/img/Cootranshuila.jpg'
        }
        if(rutas[posC].empRuta == "Flotahuila"){
            document.getElementById("txtColor").value = "Gris / Plateado"
            document.getElementById("txtImagen").src = '../../static/img/Flotahuila.jpg'
        }
        if(rutas[posC].empRuta == "Cootransneiva"){
            document.getElementById("txtColor").value = "Blanco con Rojo"
            document.getElementById("txtImagen").src = '../../static/img/CootransNeiva.jpg'
        }
        if(rutas[posC].empRuta == "Autobuses"){
            document.getElementById("txtColor").value = "Verde Oscuro"
            document.getElementById("txtImagen").src = '../../static/img/AutobuseseKool.jpg'
        }
        document.getElementById("txtEmpresa").value = rutas[posC].empRuta
        document.getElementById("txtHora").value = rutas[posC].horRuta
        document.getElementById("txtNumero").value = rutas[posC].numRuta
        waypoints.push(L.latLng(entradaR.latitud, entradaR.longitud));
    }   
  });

  // Establecer el arreglo de waypoints en el control de enrutamiento
  control.setWaypoints(waypoints);

  control.hide();
}


function cargarRutas(idRuta,numRuta,empRuta,horRuta){
    const ruta = {
        "id" : idRuta,
        "numRuta" : numRuta,
        "empRuta":empRuta,
        "horRuta":horRuta
    }
    rutas.push(ruta);
    
}

function cargasCoodernadas(idRuta,latitud,longitud,){
    const coordenada = {
        "idRuta" : idRuta,
        "latitud" : latitud,
        "longitud" : longitud
    }
    coodernadas.push(coordenada);
}