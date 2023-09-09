let rutas = []
let coodernadas = []
let comentarios = []
let ubicaciones = []
let favoritos = []

var map = L.map('map').setView([2.9341049606236704, -75.28170112926662], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

document.getElementById('ruta').addEventListener('change', function () {
    var site = this.value;
    removeRoute();
    updateRoute(site);
    mostrarDatosTabla()
});

document.getElementById('cbBarrio').addEventListener('change', function () {
    document.getElementById("ruta").innerHTML = ""
    filtroBarrio()
});
document.getElementById('cbComuna').addEventListener('change', function () {
    document.getElementById("ruta").innerHTML = ""
    filtroComuna()
});
document.getElementById('cbSitioDeInteres').addEventListener('change', function () {
    document.getElementById("ruta").innerHTML = ""
    filtroSitio()
});

$(function () {
    //se utiliza para las peticiones ajax con query
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    $("#btnFavorito").click(function () {
        verFavoritos();
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

var control;


function removeRoute() {
    if (control) {
        control.remove();
    }
}

function updateRoute(site) {
    var options = {
        lineOptions: {
            styles: [{ color: '#46668d' }]
        },
        addWaypoints: false,
        createMarker: function () { return null; },
        draggableWaypoints: false,
        fitSelectedRoutes: 'smart',
        showAlternatives: false
    };

    control = L.Routing.control(options).addTo(map);
    // Crear un arreglo para almacenar las coordenadas
    var waypoints = [];
    numeroRut = document.getElementById("ruta").value
    //Guardar ruta en local Storage
    var cantidad = 1;

    // Obtener los datos existentes del almacenamiento local
    var rutasGuardadas = JSON.parse(localStorage.getItem('datos') || '[]');

    // Verificar si la opción ya existe en el arreglo
    var opcionExistente = rutasGuardadas.find(function(item) {
      return item.ruta === numeroRut;
    });

    if (opcionExistente) {
      // Si la opción ya existe, aumentar la cantidad
      opcionExistente.cantidad += cantidad;
    } else {
      // Si la opción no existe, agregarla al arreglo
      rutasGuardadas.push({
        ruta: numeroRut,
        cantidad: cantidad
      });
    }

    // Guardar los datos actualizados en el almacenamiento local
    localStorage.setItem('datos', JSON.stringify(rutasGuardadas));

    let datos = "";
    // Recorrer el arreglo de comentarios para mostrarlos
    comentarios.forEach(entradaC => {
        if (entradaC.comRuta == numeroRut){
            
            datos += `
            
            <div class="card text-center"" style="width: 18rem;">
                            <div class="card-body">
                            <h5 class="card-title">${entradaC.conUsuario}</h5>
                            <p class="card-text">${entradaC.comDescripcion}</p>
                            <div class="testimonial-text testimonios" data-valoracion="${entradaC.comValoracion}">
                                <div class="reseñas">
                                </div>
                            </div>
                            <p class="card-text">Ruta ${entradaC.comRuta}</p>
                            </div>
                        </div>`;
        }
    });
    document.getElementById("comentarios").innerHTML=datos
    // Recorrer el arreglo de coordenadas y agregar cada punto al arreglo de waypoints
    coodernadas.forEach(entradaR => {
        posR = rutas.findIndex(ruta => ruta.numRuta == entradaR.idRuta);
        if (rutas[posR].numRuta == numeroRut) {
            if (rutas[posR].preRuta == 2400){
                if (rutas[posR].empRuta == "Coomotor") {
                    document.getElementById("txtColor").value = "Azul"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Nuevas/RUTANUEVACOOMOTOR.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Nuevas/RUTANUEVACOOMOTROLADO.jpg'
                }
                if (rutas[posR].empRuta == "CootransHuila") {
                    document.getElementById("txtColor").value = "Verde Claro con Blanco"
                    document.getElementById("txtImagenFrente").src = ''
                    document.getElementById("txtImagenLado").src = ''
                }
                if (rutas[posR].empRuta == "FlotaHuila") {
                    document.getElementById("txtColor").value = "Gris / Plateado"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Nuevas/RUTANUEVAFLOTA.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Nuevas/RUTANUEVAFLOTALADO.jpg'
                }
                if (rutas[posR].empRuta == "CootransNeiva") {
                    document.getElementById("txtColor").value = "Blanco con Rojo"
                    document.getElementById("txtImagenFrente").src = ''
                    document.getElementById("txtImagenLado").src = ''
                }
                if (rutas[posR].empRuta == "AutoBuses") {
                    document.getElementById("txtColor").value = "Verde Oscuro"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Nuevas/RUTANUEVAAUTOBUSES.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Nuevas/RUTANUEVAAUTOBUSESLADO.jpg'
                }
            }
            if (rutas[posR].preRuta == 2300){
                if (rutas[posR].empRuta == "Coomotor") {
                    document.getElementById("txtColor").value = "Azul"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOMOTOR.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOMOTORLADO.jpg'
                }
                if (rutas[posR].empRuta == "CootransHuila") {
                    document.getElementById("txtColor").value = "Verde Claro con Blanco"
                    document.getElementById("txtImagenFrente").src = ''
                    document.getElementById("txtImagenLado").src = ''
                }
                if (rutas[posR].empRuta == "FlotaHuila") {
                    document.getElementById("txtColor").value = "Gris / Plateado"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Viejas/RUTAVIEJAFLOTA.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Viejas/RUTAVIEJAFLOTALADO.jpg'
                }
                if (rutas[posR].empRuta == "CootransNeiva") {
                    document.getElementById("txtColor").value = "Blanco con Rojo"
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOTRANSNEIVA'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOTRANSNEIVALADO'
                }
                if (rutas[posR].empRuta == "AutoBuses") {
                    document.getElementById("txtColor").value = "Verde Oscuro"
                    document.getElementById("txtImagenFrente").src = ''
                    document.getElementById("txtImagenLado").src = ''
                }
            }
            
            document.getElementById("txtEmpresa").value = rutas[posR].empRuta
            document.getElementById("txtPrecio").value = "$"+rutas[posR].preRuta
            document.getElementById("txtNumero").value = rutas[posR].numRuta
            waypoints.push(L.latLng(entradaR.latitud, entradaR.longitud));
        }
    });

    // Establecer el arreglo de waypoints en el control de enrutamiento
    control.setWaypoints(waypoints);

    control.hide();
    $(document).ready(function () {
        $('.testimonios').each(function () {
          const valoracion = $(this).data('valoracion');
          const reseñasContainer = $(this).find('.reseñas');
    
          for (let i = 1; i <= 5; i++) {
            if (i <= valoracion) {
              reseñasContainer.append('<i class="fa fa-heart hearto"></i>');
            } else {
              reseñasContainer.append('<i class="fa fa-heart hearti"></i>');
            }
          }
        });
      });
}

function filtroBarrio() {
    let rutasAgregadas = [];
    ubiBarrio = document.getElementById("cbBarrio").value
    document.getElementById("ruta").innerHTML += `<option value="0" disabled selected>Seleccione</option>`
    ubicaciones.forEach(entradaU => {
        if (entradaU.ubiBarrio == ubiBarrio) {
            posU = rutas.findIndex(ruta => ruta.numRuta === entradaU.ubiRuta);       
            console.log(posU)
            if (!rutasAgregadas.includes(rutas[posU].numRuta)) {
                rutasAgregadas.push(rutas[posU].numRuta)
                document.getElementById("ruta").innerHTML += `<option value="${rutas[posU].numRuta}">Ruta ${rutas[posU].numRuta}</option>`
            }
        }
    })
    if (ubiBarrio == "0") {
        document.getElementById("ruta").innerHTML = ""
        document.getElementById("ruta").innerHTML = `<option value="0">Seleccione</option>`
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

function filtroComuna() {
    let rutasAgregadas = [];
    ubiComuna = document.getElementById("cbComuna").value
    document.getElementById("ruta").innerHTML += `<option value="0" disabled selected>Seleccione</option>`
    ubicaciones.forEach(entradaU => {
        if (entradaU.ubiComuna == ubiComuna) {
            posU = rutas.findIndex(ruta => ruta.numRuta === entradaU.ubiRuta);
            if (!rutasAgregadas.includes(rutas[posU].numRuta)) {
                rutasAgregadas.push(rutas[posU].numRuta)
                document.getElementById("ruta").innerHTML += `<option value="${rutas[posU].numRuta}">Ruta ${rutas[posU].numRuta}</option>`
            }
        }
    })
    if (ubiComuna == "0") {
        document.getElementById("ruta").innerHTML = ""
        document.getElementById("ruta").innerHTML = `<option value="0">Seleccione</option>`
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

function filtroSitio() {
    let rutasAgregadas = [];
    ubiSitioDeInteres = document.getElementById("cbSitioDeInteres").value
    document.getElementById("ruta").innerHTML += `<option value="0" disabled selected>Seleccione</option>`
    ubicaciones.forEach(entradaU => {
        if (entradaU.ubiSitioDeInteres == ubiSitioDeInteres) {
            posU = rutas.findIndex(ruta => ruta.numRuta === entradaU.ubiRuta);
            if (!rutasAgregadas.includes(rutas[posU].numRuta)) {
                rutasAgregadas.push(rutas[posU].numRuta)
                document.getElementById("ruta").innerHTML += `<option value="${rutas[posU].numRuta}">Ruta ${rutas[posU].numRuta}</option>`
            }

        }
    })
    if (ubiSitioDeInteres == "0") {
        document.getElementById("ruta").innerHTML = ""
        document.getElementById("ruta").innerHTML = `<option value="0">Seleccione</option>`
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

function cargarComentarios(comDescripcion, conUsuario, conValoracion, comRuta) {
    const comentario = {
        "comDescripcion": comDescripcion,
        "conUsuario": conUsuario,
        "comValoracion": conValoracion,
        "comRuta": comRuta
    }
    comentarios.push(comentario);

}

function cargarRutas(idRuta, numRuta, empRuta, preRuta) {
    const ruta = {
        "id": idRuta,
        "numRuta": numRuta,
        "empRuta": empRuta,
        "preRuta": preRuta
    }
    rutas.push(ruta);

}

function cargasCoodernadas(idRuta, latitud, longitud,) {
    const coordenada = {
        "idRuta": idRuta,
        "latitud": latitud,
        "longitud": longitud
    }
    coodernadas.push(coordenada);
}

function cargarUbicaciones(id, ubiBarrio, ubiComuna, ubiSitioDeInteres, ubiRuta) {
    const ubicacion = {
        "id": id,
        "ubiBarrio": ubiBarrio,
        "ubiComuna": ubiComuna,
        "ubiSitioDeInteres": ubiSitioDeInteres,
        "ubiRuta": ubiRuta
    }
    ubicaciones.push(ubicacion);

}

function cargarFavorito(ruta, usuario) {
    const favorito = {
        "ruta": ruta,
        "usuario": usuario,
    }
    favoritos.push(favorito);
}

function verFavoritos() {
    $.ajax({
        url: '/verificarSesion/',
        method: 'GET',
        success: function (data) {
            console.log(data)
            if (data.logueado) {
                // Si el usuario ha iniciado sesión, muestra el modal.
                mostrarFavoritos()
                
            } else {
                // Si el usuario no ha iniciado sesión, muestra un mensaje de error.
                Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error');
            }
        }
    });
}

function mostrarFavoritos() {
    document.getElementById("RutasFavoritas").innerHTML = ""
    favoritos.forEach(entradaF => {
        posF = rutas.findIndex(ruta => ruta.numRuta == entradaF.ruta);
        console.log(rutas[posF].numRuta)
        document.getElementById("RutasFavoritas").innerHTML += `<div class="form-group row testimonios_contenedor">
                                                        <div class="mb-1 col-lg-6 comentarios_clientes">
                                                            Ruta: ${rutas[posF].numRuta}
                                                            <br>
                                                            Empresa: ${rutas[posF].empRuta}
                                                        </div>
                                                        <div class="mb-1 col-lg-2 justify-content-end">
                                                            <button type="button" class="btn btn-inicio" onclick="vizualizarRutaFavorita(${rutas[posF].numRuta})">Visualizar</button>
                                                        </div>
                                                        <div class="mb-1 ml-5 col-lg-2 justify-content-end">
                                                            <button type="button" class="btn btn-custom" onclick="eliminarFavorito(${rutas[posF].numRuta})">Eliminar</button>
                                                        </div>
                                                    </div>
                                                    <hr>`
    })
}

function vizualizarRutaFavorita(numeroRuta) {
    removeRoute();
    var options = {
        lineOptions: {
            styles: [{ color: '#46668d' }]
        },
        addWaypoints: false,
        createMarker: function () { return null; },
        draggableWaypoints: false,
        fitSelectedRoutes: 'smart',
        showAlternatives: false
    };

    control = L.Routing.control(options).addTo(map);
    // Crear un arreglo para almacenar las coordenadas
    var waypoints = [];
    // Recorrer el arreglo de coordenadas y agregar cada punto al arreglo de waypoints
    coodernadas.forEach(entradaR => {
        posC = rutas.findIndex(ruta => ruta.numRuta == entradaR.idRuta);
        if (rutas[posC].numRuta == numeroRuta) {
            if (rutas[posC].empRuta == "Coomotor") {
                document.getElementById("txtColor").value = "Azul"
                document.getElementById("txtImagen").src = '../../static/img/Coomotor.jpg'
            }
            if (rutas[posC].empRuta == "Cootranshuila") {
                document.getElementById("txtColor").value = "Verde Claro con Blanco"
                document.getElementById("txtImagen").src = '../../static/img/Cootranshuila.jpg'
            }
            if (rutas[posC].empRuta == "Flotahuila") {
                document.getElementById("txtColor").value = "Gris / Plateado"
                document.getElementById("txtImagen").src = '../../static/img/Flotahuila.jpg'
            }
            if (rutas[posC].empRuta == "Cootransneiva") {
                document.getElementById("txtColor").value = "Blanco con Rojo"
                document.getElementById("txtImagen").src = '../../static/img/CootransNeiva.jpg'
            }
            if (rutas[posC].empRuta == "Autobuses") {
                document.getElementById("txtColor").value = "Verde Oscuro"
                document.getElementById("txtImagen").src = '../../static/img/AutobuseseKool.jpg'
            }
            document.getElementById("txtEmpresa").value = rutas[posC].empRuta
            document.getElementById("txtPrecio").value = rutas[posC].preRuta
            document.getElementById("txtNumero").value = rutas[posC].numRuta
            waypoints.push(L.latLng(entradaR.latitud, entradaR.longitud));
        }
    });

    // Establecer el arreglo de waypoints en el control de enrutamiento
    control.setWaypoints(waypoints);
    control.hide();
}

function eliminarFavorito(NumeroRuta) {
  var datos = {
    "numeroRuta": NumeroRuta,
  }
  $.ajax({
    url: "/eliminarFavorito/",
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

function hacerGrafica() {
   var ruta=[];
   var cantidad=[];
   // Obtén los datos de local storage
   var dataString = localStorage.getItem("datos");

   // Convierte la cadena JSON en un arreglo de objetos JavaScript
   var data = JSON.parse(dataString);
   
   // Verifica si los datos son un arreglo
   if (Array.isArray(data)) {
       // Itera sobre la lista de objetos
       for (var i = 0; i < data.length; i++) {
           var elemento = data[i];
           
           // Accede a los valores de "ruta" y "cantidad" para cada elemento
            ruta.push("Ruta"+" "+elemento.ruta);
            cantidad.push(parseInt(elemento.cantidad));
           
           
       }
   } else {
       console.log("Los datos no son un arreglo o están vacíos.");
   }
   var datos = {
    "ruta": JSON.stringify(ruta),
    "cantidad": JSON.stringify(cantidad),
  }
   console.log(datos)
   $.ajax({
    url: "/realizarGrafica/",
    data: datos,
    type: 'GET',
    dataType: 'json',
    cache: false,
    success: function (resultado) {
        window.location.reload();
    }
  })
}

