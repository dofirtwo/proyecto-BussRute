$(function () {
  $("#fileFoto").on("change", validar);
})

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

document.addEventListener("DOMContentLoaded", function () {
  trazarRuta();
});

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

    // Mostrar coordenadas en la consola
    console.log('Latitud:', latlng.lat);
    console.log('Longitud:', latlng.lng);
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
            styles: [{ color: '#00A99D' }]
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


function registroDatosRuta() {
  var datos = {
    "numeroRuta": $("#txtNumeroRuta").val(),
    "horario": $("#txtPrecio").val(),
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

function agregarDetalleSolicitud(latitud, Longitud) {
  const elemento = {
    "numeroRuta": $("#txtNumeroRuta").val(),
    "latitud": latitud,
    "longitud": Longitud,
  }
  coordenadaRuta.push(elemento);
  mostrarDatosTabla()
}

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

function validar(evt) {
  let files = evt.target.files
  let file = files[0]
  let url = URL.createObjectURL(file)
  $("#imagenProducto").attr("src", url)

  let fileName = files[0].name
  let fileSize = files[0].size
  let extension = fileName.split('.').pop()
  extension = extension.toLowerCase()
  if (extension != "jpg") {
    Swal.fire({ title: 'Problemas', text: "Solo se pueden cargar Imagenes con extension .jpg", icon: 'error', })
    $("#fileFoto").val("")
  } else if (fileSize > "50000") {
    Swal.fire({ title: 'Problemas', text: "Solo se pueden cargar Imagenes mayores a 50Kb .jpg", icon: 'error', })
    $("#fileFoto").val("")
  }
}

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

function agregarUbicacion() {
  barrio = document.getElementById("cbBarrio").value
  comuna = document.getElementById("cbComuna").value
  sitio = document.getElementById("cbSitioDeInteres").value
  cargarUbicacion(barrio, comuna, sitio)
}

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

function abrirModalEliminar(id){
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
      console.log(resultado);
      window.location.reload();
      Swal.fire("Registro de Solicitud", resultado.mensaje, "success")
    }
  })
}