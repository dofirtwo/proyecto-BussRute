let rutas = []
let coodernadas = []
let comentarios = []
let ubicaciones = []
let favoritos = []

//Json de los sitios de interes para lograr bordearlos mediante la api (con su logintud y latitud)
let sitios = [
    {
        nombre: "Estadio Guillermo Plazas Alcid",
        coordenadas: [
            [2.937096, -75.280227],   
            [2.936764, -75.281488], 
            [2.936202, -75.281423],  
            [2.934809, -75.280806], 
            [2.935168, -75.279310], 
            [2.936764, -75.279685], 
        ],
        weight: 1
    },
    {
        nombre: "Hospital General",
        coordenadas: [
            [2.933915, -75.281020],
            [2.933291, -75.281966],
            [2.930875, -75.281164],
            [2.930832, -75.281127],
            [2.931496, -75.280317],
            [2.931676, -75.280100],
            [2.933889, -75.280971]
        ],
        weight: 1
    },
    {
        nombre: "Cementario",
        coordenadas: [
            [2.935137, -75.294844],
            [2.935067, -75.295029],
            [2.934207, -75.296829],
            [2.932970, -75.296086],
            [2.933587, -75.294669],
            [2.933884, -75.294234]
        ],
        weight: 1
    },
    {
        nombre: "Biblioteca Banco de la Republica",
        coordenadas: [
            [2.925263, -75.288289],  
            [2.925121, -75.288658], 
            [2.924864, -75.288557],  
            [2.924993, -75.288192], 
        ],
        weight: 1
    },
    {
        nombre: "Parque Leesburg",
        coordenadas: [
            [2.937551, -75.289330],  
            [2.937221, -75.290126], 
            [2.936755, -75.290024],  
            [2.936889, -75.289254], 
        ],
        weight: 1
    },
    {
        nombre: "Centro Comercial San Pedro Plaza",
        coordenadas: [
            [2.950750, -75.287006],  
            [2.952571, -75.287711], 
            [2.950868, -75.289755],  
            [2.950621, -75.289539], 
            [2.950392, -75.289325], 
            [2.950068, -75.289083], 
            [2.949837, -75.288947], 
            [2.949597, -75.288835], 
            [2.948754, -75.288458], 
            [2.948623, -75.288490], 
            [2.948363, -75.288451], 
        ],
        weight: 1
    },
    {
        nombre: "La Cruz Roja",
        coordenadas: [
            [2.942958, -75.293270],  
            [2.943104, -75.293900], 
            [2.941589, -75.294304],  
            [2.941495, -75.294296], 
            [2.941646, -75.294243],  
            [2.941804, -75.294159], 
            [2.941854, -75.294113],  
            [2.941927, -75.294005],
            [2.942039, -75.293732],
            [2.942071, -75.293616],
            [2.942110, -75.293254],
        ],
        weight: 1
    },
    {
        nombre: "Universidad Antonio Ñariño",
        coordenadas: [
            [2.940017, -75.255730],  
            [2.940048, -75.256516], 
            [2.940058, -75.256805],  
            [2.940163, -75.257485], 
            [2.938842, -75.257492],  
            [2.938834, -75.255797], 
        ],
        weight: 1
    },
    {
        nombre: "Canchas El Jardin",
        coordenadas: [
            [2.940614, -75.268698],  
            [2.940595, -75.269305], 
            [2.939758, -75.269313],  
            [2.939781, -75.268656], 
        ],
        weight: 1
    },
    {
        nombre: "Coca-Cola",
        coordenadas: [
            [2.954642, -75.297719],  
            [2.955389, -75.301990], 
            [2.954181, -75.302167],  
            [2.953447, -75.297907], 
        ],
        weight: 1
    },
    {
        nombre: "Terminal de Trasportes",
        coordenadas: [
            [2.918369, -75.280876],
            [2.918363, -75.281518], 
            [2.918265, -75.281590],  
            [2.918227, -75.281739], 
            [2.918264, -75.282755], 
            [2.917948, -75.282967], 
            [2.916646, -75.283001], 
            [2.916350, -75.283030],  
            [2.916243, -75.283065], 
            [2.916104, -75.283181], 
            [2.916081, -75.283179], 
            [2.915365, -75.282635], 
            [2.915323, -75.282188],  
            [2.915264, -75.281860], 
            [2.915264, -75.281860], 
            [2.915240, -75.281615],  
            [2.915264, -75.281578], 
            [2.915307, -75.281614],           
            [2.915677, -75.281528],
            [2.916168, -75.281332],
            [2.916738, -75.281025],         
            [2.917159, -75.280712], 
            [2.917334, -75.280886], 
            [2.917473, -75.280938], 
        ],
        weight: 1
    },
    // Puedes agregar más cuadrados aquí
];

//Inicializa la api para que muestre un mapa en unas coordenadas deseadas
//en este caso Neiva
var map = L.map('map').setView([2.9341049606236704, -75.28170112926662], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

//evento para cuando se seleccione una ruta y esta se pueda vizualizar
document.getElementById('ruta').addEventListener('change', function () {
    ocultarRuta();
    if (document.getElementById('ruta').value == 0){
        document.getElementById("txtEmpresa").value = ""
        document.getElementById("txtPrecio").value = ""
        document.getElementById("txtNumero").value = ""
        document.getElementById("comentarios").innerHTML=""
        document.getElementById("txtColor").value = ""
        document.getElementById("txtImagenFrente").src = ""
        document.getElementById("txtImagenLado").src = ""
    } else{
        mostrarRuta();
    }
});

//evento cuando se seleccione la opcion de mostrar las Rutas que pasan cerca
//de la Ubicacion actual del Usuario
document.getElementById('btnUbicacion').addEventListener('change', function () {
    if (this.checked) {
        mostrarRutasCercanas();
    } else {
        document.getElementById("ruta").innerHTML = ""
        document.getElementById("ruta").innerHTML = `<option value="0">Seleccione</option>`
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }
});

//eventos para cuando se seleccione alguno de los filtros(Barrio,Comuna,Sitio de Interes)  
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

/**
 * Funcion para ocutar la ruta que se encuentra visible
 */
function ocultarRuta() {
    if (control) {
        control.remove();
    }
}

/**
 * Funcion para caclular la distancia entre un punto de la ruta y la ubicacion acutal de Usuario
 * @param {Double} lat1 latitud en la cual se encuentra el Usuario
 * @param {Double} lon1 longitud en la cual se encuentra el Usuario
 * @param {Double} lat2 latitud en la cual se encuentra un Punto de la Ruta
 * @param {Double} lon2 longitud en la cual se encuentra un Punto de la Ruta
 * @returns 
 */
function haversine(lat1, lon1, lat2, lon2) {
    // Radio de la Tierra en kilómetros
    var R = 6371;

    // Convierte las coordenadas de grados a radianes
    var lat1Rad = (lat1 * Math.PI) / 180;
    var lon1Rad = (lon1 * Math.PI) / 180;
    var lat2Rad = (lat2 * Math.PI) / 180;
    var lon2Rad = (lon2 * Math.PI) / 180;

    // Diferencias entre las coordenadas
    var dLat = lat2Rad - lat1Rad;
    var dLon = lon2Rad - lon1Rad;

    // Fórmula haversine
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1Rad) * Math.cos(lat2Rad) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    // Distancia en kilómetros
    var distance = R * c;

    return distance;
}


/**
 * Funcion encargada de mostrar las rutas cercanas a la ubicacion actual de Usuario
 */
function mostrarRutasCercanas() {
    // Limpia el contenido actual del elemento <select>
    document.getElementById("ruta").innerHTML = `<option value="0" disabled selected>Seleccione</option>`;

    // Crear un objeto para mantener un registro de las rutas
    var rutasAgregadas = {};

    coodernadas.forEach(entradaR => {
        navigator.geolocation.getCurrentPosition(function (position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            // Calcula la distancia entre tu ubicación y el punto específico
            var distancia = haversine(lat, lon, entradaR.latitud, entradaR.longitud);

            // Define un umbral de distancia (en kilómetros)
            var umbral = 1.0; // Por ejemplo, 1 kilómetro
            // Compara la distancia con el umbral
            if (distancia <= umbral) {
                posU = rutas.findIndex(ruta => ruta.numRuta == entradaR.idRuta);
                // Verifica si esta ruta ya ha sido agregada antes
                if (!rutasAgregadas[rutas[posU].numRuta]) {
                    // Agrega la ruta al elemento <select>
                    document.getElementById("ruta").innerHTML += `<option value="${rutas[posU].numRuta}">Ruta ${rutas[posU].numRuta}</option>`;

                    // Marca la ruta como agregada en el registro
                    rutasAgregadas[rutas[posU].numRuta] = true;
                }
            }
        }, function (error) {
            // Manejo de errores de geolocalización
            console.error('Error de geolocalización:', error);
        });
    });
}

/**
 * Funcion encargada de Trazar la Ruta en el mapa y mostrar los valores de la ruta seleccionada (Nombre,Precio,Color,imagenes,Numero de Ruta)
 * tambien muestra los Comentarios que se tienen relacionados con la Ruta (Si es que esta tiene)
 * y por ultimo muestra en la mapa los sitios de interes por donde para la Ruta (Estos se muestran de un color) 
 */
function mostrarRuta() {
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });
    ubicacionDispositivo()
    map.eachLayer(function(layer) {
        if (layer instanceof L.Polygon) {
            map.removeLayer(layer);
        }
    });
    
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
    
    ubicaciones.forEach(entradaC => {
        if (entradaC.ubiRuta == numeroRut){
            sitios.forEach(function(cuadrado) {
                if(cuadrado.nombre == entradaC.ubiSitioDeInteres){
                    var polygon = L.polygon(cuadrado.coordenadas, { color:"#6f7fe2 ", weight: cuadrado.weight }).addTo(map);
                    // Calcular las coordenadas del centro del cuadrado
                    var squareCenter = polygon.getBounds().getCenter();

                    // Crear un marcador en el centro del cuadrado
                    var marker = L.marker(squareCenter).addTo(map);
                    polygon.bindPopup(cuadrado.nombre); // Agregar nombre como etiqueta emergente
                }
               
            });
        }
    });


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
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Nuevas/RUTANUEVAVCOOMOTOR.jpg'
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
                    document.getElementById("txtImagenFrente").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOTRANSNEIVA.jpg'
                    document.getElementById("txtImagenLado").src = '../../static/img/Buses/Viejas/RUTAVIEJACOOTRANSNEIVALADO.jpg'
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

/**
 * Esta funcion es la encargada de ser un filtro por Barrios, mostrando las rutas que pasan por este
 * cuando no se selecciona un Barrio esta volvera a mostrar todas las Rutas
 */
function filtroBarrio() {
    let rutasAgregadas = [];
    ubiBarrio = document.getElementById("cbBarrio").value
    document.getElementById('cbSitioDeInteres').disabled = true;
    document.getElementById('cbComuna').disabled = true;
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
        document.getElementById('cbSitioDeInteres').disabled = false;
        document.getElementById('cbComuna').disabled = false;
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

/**
 * Esta funcion es la encargada de ser un filtro por Comunas, mostrando las rutas que pasan por este
 * cuando no se selecciona un Comuna esta volvera a mostrar todas las Rutas
 */
function filtroComuna() {
    let rutasAgregadas = [];
    ubiComuna = document.getElementById("cbComuna").value
    document.getElementById('cbBarrio').disabled = true;
    document.getElementById('cbSitioDeInteres').disabled = true;
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
        document.getElementById('cbBarrio').disabled = false;
        document.getElementById('cbSitioDeInteres').disabled = false;
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

/**
 * Esta funcion es la encargada de ser un filtro por los Sitios de Interes, mostrando las rutas que pasan por este
 * cuando no se selecciona un Sitio de Interes esta volvera a mostrar todas las Rutas
 */
function filtroSitio() {
    let rutasAgregadas = [];
    ubiSitioDeInteres = document.getElementById("cbSitioDeInteres").value
    document.getElementById('cbBarrio').disabled = true;
    document.getElementById('cbComuna').disabled = true;
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
        document.getElementById('cbBarrio').disabled = false;
        document.getElementById('cbComuna').disabled = false;
        rutas.forEach(entradaR => {
            document.getElementById("ruta").innerHTML += `<option value="${entradaR.numRuta}">Ruta ${entradaR.numRuta}</option>`
        })
    }

}

/**
 * Funcion encargada de Cargar los Comentarios existenten en la base de datos
 * @param {String} comDescripcion Contenido del Comentario
 * @param {String} conUsuario Usuario que realizo el Comentario
 * @param {Int} conValoracion Valoracion que el Usuario le dio al Comentario
 * @param {Int} comRuta Ruta a la cual el Usuario realizo el Comentario
 */
function cargarComentarios(comDescripcion, conUsuario, conValoracion, comRuta) {
    const comentario = {
        "comDescripcion": comDescripcion,
        "conUsuario": conUsuario,
        "comValoracion": conValoracion,
        "comRuta": comRuta
    }
    comentarios.push(comentario);

}

/**
 * Funcion encargada de Cargar las Rutas existenten en la base de datos
 * @param {Int} idRuta Id de la ruta
 * @param {Int} numRuta Numero que la Ruta tiene
 * @param {String} empRuta Empresa que dueña de la Ruta
 * @param {Int} preRuta Precio que tiene la Ruta
 */
function cargarRutas(idRuta, numRuta, empRuta, preRuta) {
    const ruta = {
        "id": idRuta,
        "numRuta": numRuta,
        "empRuta": empRuta,
        "preRuta": preRuta
    }
    rutas.push(ruta);

}

/**
 * Funcion encargada de Cargar las Coordenadas existenten en la base de datos
 * @param {Int} idRuta 
 * @param {Double} latitud 
 * @param {Double} longitud 
 */
function cargasCoodernadas(idRuta, latitud, longitud,) {
    const coordenada = {
        "idRuta": idRuta,
        "latitud": latitud,
        "longitud": longitud
    }
    coodernadas.push(coordenada);
}

/**
 * Funcion encargada de Cargar las Ubicaciones existenten en la base de datos
 * @param {Int} id Id de la Ubicacion
 * @param {String} ubiBarrio Barrio donde se encuentra la Ubicacion
 * @param {String} ubiComuna Comuna donde se encuentra la Ubicacion
 * @param {String} ubiSitioDeInteres Sitio de Interes donde se encuentra la Ubicacion
 * @param {Int} ubiRuta Ruta la cual pasa por la Ubicacion
 */
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

/**
 * Funcion encargada de Cargar los Favoritos existenten en la base de datos
 * @param {Int} ruta Ruta la cual fue Guardada en Favorito
 * @param {Int} usuario Usuario el cual Guardo la Ruta en Favorito
 */
function cargarFavorito(ruta, usuario) {
    const favorito = {
        "ruta": ruta,
        "usuario": usuario,
    }
    favoritos.push(favorito);
}

/**
 * Esta funcion se encarga de verificar si el Usuario esta en session y si es asi muestra la modal de Favoritos
 */
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

/**
 * Esta Funcion se encarga de crear una modal con las Rutas Favoritas 
 */
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

/**
 * Esta funcion se encarga de Vizualizar la Ruta Favorita que se seleccione 
 * @param {Int} numeroRuta Numero de la Ruta Favorita
 */
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

/**
 * Esta funcion se encarga de Eliminar la Ruta Favorita que se seleccione 
 * @param {Int} NumeroRuta Numero de la Ruta Favorita
 */
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

/**
 * Esta funcion se encarga de guardar la cantidad de veces que se selecciona una ruta en el Local Storage
 * para posteriormente graficar los datos
 */
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
        location.href = `/verGraficas/`;
    }
  })
}

/**
 * Esta funcion se encarga de obtener la Ubicacion actual del Usuario
 */
function ubicacionDispositivo(){
    // Obtén la ubicación del dispositivo
    navigator.geolocation.getCurrentPosition(function (position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        // Crea un marcador en la ubicación del dispositivo
        L.marker([lat, lon]).addTo(map)
            .bindPopup('Tu ubicación').openPopup();
    }, function (error) {
        // Manejo de errores
        console.error('Error de geolocalización:', error);
    });
}


