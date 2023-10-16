let coodernadas = []
let coordenadaRuta = []
let ubicacionRuta = []

$(function () {
  //se utiliza para las peticiones ajax con query
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  $("#btnRegistrarRuta").click(function () {
    registroDatosRuta();
  })
})

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }

    }
  }
  return cookieValue;
}

//Este evento ejecuta la funcion cuando la pagina carga
document.addEventListener("DOMContentLoaded", function () {
  trazarRuta();
});

/**
 * Esta funcion se encarga de inicializar el mapa de la api y lograr que al momento de darle click en algun punto
 * del mapa este guarde las coordenadas (latitud, longitd) en una lista
 */
function trazarRuta() {
  // Crea un mapa
  const map = L.map('map').setView([2.9341049606236704, -75.28170112926662], 13);
  // Crea una capa base
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Variables para almacenar los puntos y la ruta
  const waypoints = [];
  let markerGroup;
  let routingControl;

  // Icono personalizado
  const customIcon = L.icon({
    iconUrl: '../../static/img/images/marker-icon.png',
    shadowUrl: '../../static/img/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // Evento que se activa cuando se hace clic en el mapa
  map.on('click', (e) => {
    const latlng = e.latlng;

    agregarDetalleSolicitud(latlng.lat, latlng.lng)
    cargarCoodernada(document.getElementById("txtNumeroRuta").value, latlng.lat, latlng.lng);
    // Crea un marcador en la ubicación del clic con el icono personalizado
    const marker = L.marker(latlng, { icon: customIcon }).addTo(map);

    // Agrega el marcador al grupo de marcadores
    if (!markerGroup) {
      markerGroup = L.layerGroup([marker]).addTo(map);
    } else {
      markerGroup.addLayer(marker);
    }

    // Agrega el punto al arreglo de waypoints
    waypoints.push(latlng);

    // Si hay más de un punto, dibuja la línea de ruta
    if (waypoints.length > 1) {
      // Si ya hay un control de enrutamiento, lo elimina del mapa
      if (routingControl) {
        map.removeControl(routingControl);
      }

      // Crea una matriz de coordenadas para el enrutamiento
      const coordinates = waypoints.map((waypoint) => [waypoint.lat, waypoint.lng]);

      // Crea el control de enrutamiento
      routingControl = L.Routing.control({
        waypoints: coordinates,
        routeWhileDragging: true,
        show: false,
        addWaypoints: false,
        createMarker: function () { return null; },
        draggableWaypoints: false,
        fitSelectedRoutes: 'smart',
        showAlternatives: false,
        routeLine: (route) => {
          return L.Routing.line(route, {
            styles: [{ color: '#46668d' }]
          });
        }
      }).addTo(map);

      // Muestra la línea de ruta en el mapa
      routingControl.on('routesfound', (e) => {
        const routes = e.routes;
        const route = routes[0];
      });
    }
  });
}

/**
 * Esta funcion se encarga de mandar los datos de la Ruta, a la funcion en Python/Django
 * por Post
 */
function registroDatosRuta() {
  var datos = {
    "numeroRuta": $("#txtNumeroRuta").val(),
    "precio": $("#txtPrecio").val(),
    "empresa": $("#cbEmpresa").val(),
    "detalle": JSON.stringify(coordenadaRuta),
    "ubicacion": JSON.stringify(ubicacionRuta),
  }
  $.ajax({
    url: "/registroRuta/",
    data: datos,
    type: 'post',
    dataType: 'json',
    cache: false,
    success: function (resultado) {
      console.log(resultado);
      if (resultado.estado) {
        frmRegistrarRuta.reset();
        coordenadaRuta.length = 0;
        mostrarDatosTabla();
      }
      Swal.fire("Registro de Solicitud", resultado.mensaje, "success")
    }
  })
}

/**
 * Esta funcion se encarga de guardar las coodernadas de una punto de la ruta en una lista
 * tambien muestra en una tabla los valores que tiene esta lista
 * @param {Double} latitud latitud del punto de la Ruta
 * @param {Double} Longitud longitud del punto de la Ruta
 */
function agregarDetalleSolicitud(latitud, Longitud) {
  const elemento = {
    "numeroRuta": $("#txtNumeroRuta").val(),
    "latitud": latitud,
    "longitud": Longitud,
  }
  coordenadaRuta.push(elemento);
  mostrarDatosTabla()
}

/**
 * Esta funcion se encarga de colocar en una tabla los valores que tenga la lista de coordenadasRuta
 */
function mostrarDatosTabla() {
  datos = "";
  coordenadaRuta.forEach(entrada => {
    datos += "<tr>"
    datos += "<td class'text-center'>" + entrada.numeroRuta + "</td>"
    datos += "<td class'text-center'>" + entrada.latitud + "</td>"
    datos += "<td class'text-center'>" + entrada.longitud + "</td>"
    datos += "</tr>"
  });
  document.getElementById("datosCoodenadasRutas").innerHTML = datos;
}

function cargarCoodernada(numRuta, Latitud, Longitud) {
  const coodernada = {
    "numeroRuta": numRuta,
    "Latitud": Latitud,
    "Longitud": Longitud,
  }
  coodernadas.push(coodernada);
  console.log(coodernadas)
}

/**
 * Esta funcion se encarga de llenar la lista de ubicacionRuta con datos
 * tambien se encarga de mostrar en una tabla
 * @param {String} barrio Barrio de la Ubicacion
 * @param {String} comuna Comuna de la Ubicacion
 * @param {String} sitio Sitio de Interes de la Ubicacion
 */
function cargarUbicacion(barrio, comuna, sitio) {
  const ubicacion = {
    "numeroRuta": $("#txtNumeroRuta").val(),
    "barrio": barrio,
    "comuna": comuna,
    "sitioDeInteres": sitio,
  }
  ubicacionRuta.push(ubicacion);
  mostrarDatosUnicacionTabla()
}

/**
 * esta funcion se encarga de enviar los datos a la funcion de cargarUbicacion
 */
function agregarUbicacion() {
  barrio = document.getElementById("cbBarrio").value
  comuna = document.getElementById("cbComuna").value
  sitio = document.getElementById("cbSitioDeInteres").value
  cargarUbicacion(barrio, comuna, sitio)
}

/**
 * Esta funcion se encarga de colocar en una tabla los valores que tenga la lista de ubicacionRuta
 */
function mostrarDatosUnicacionTabla() {
  datos = "";
  ubicacionRuta.forEach(entrada => {
    datos += "<tr>"
    datos += "<td class'text-center'>" + entrada.numeroRuta + "</td>"
    datos += "<td class'text-center'>" + entrada.barrio + "</td>"
    datos += "<td class'text-center'>" + entrada.comuna + "</td>"
    datos += "<td class'text-center'>" + entrada.sitioDeInteres + "</td>"
    datos += "</tr>"
  });
  document.getElementById("datosUbicacionRutas").innerHTML = datos;
}

/**
 * Esta funcion se encarga de abrir una modal para al momento de eliminar pueda tomar la decision final
 * y si el selecciona que "Si" ejecuta la funcion eliminarRuta()
 * @param {Int} id Id de la Ruta
 */
function abrirModalEliminar(id) {
  Swal.fire({
    title: 'Eliminar Ruta',
    text: "¿Estan seguros de eliminar?",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    cancelButtonText: 'No',
    confirmButtonText: 'Si'
  }).then((result) => {
    if (result.isConfirmed) {
      eliminarRuta(id)
    }
  })
}

/**
 * Esta funcion de encarga de Realizar una peticion a Python/Django para eliminar una ruta de la base de datos
 * @param {Int} id Id de la Ruta
 */
function eliminarRuta(id) {
  var datos = {
    "id": id,
  }
  $.ajax({
    url: "/eliminarRuta/",
    data: datos,
    type: 'post',
    dataType: 'json',
    cache: false,
    success: function (resultado) {
      Swal.fire("Registro de Solicitud", resultado.mensaje, "success")
        .then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
    }
  })
}

/**
 * Esta funcion se encarga de Realizar una peticion a Python/Django para cambiar el estado de la ruta
 * ya sea de (A) a (I) o de (I) a (A)
 * @param {Int} id Id de la Ruta
 */
function cambiarEstado(id) {
  $.ajax({
    url: '/vistaListaNuevo/',
    type: 'POST',
    data: {
      'id': id,
      'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
  });
}