let rutas = []
let coodernadas = []
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
            styles: [{ color: '#00A99D' }]
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
    // Recorrer el arreglo de coordenadas y agregar cada punto al arreglo de waypoints
    coodernadas.forEach(entradaR => {
        posC = rutas.findIndex(ruta => ruta.numRuta == entradaR.idRuta);
        if (rutas[posC].numRuta == numeroRut) {
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
            document.getElementById("txtHora").value = rutas[posC].horRuta
            document.getElementById("txtNumero").value = rutas[posC].numRuta
            waypoints.push(L.latLng(entradaR.latitud, entradaR.longitud));
        }
    });

    // Establecer el arreglo de waypoints en el control de enrutamiento
    control.setWaypoints(waypoints);

    control.hide();
}

function filtroBarrio() {
    let rutasAgregadas = [];
    ubiBarrio = document.getElementById("cbBarrio").value
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


function cargarRutas(idRuta, numRuta, empRuta, horRuta) {
    const ruta = {
        "id": idRuta,
        "numRuta": numRuta,
        "empRuta": empRuta,
        "horRuta": horRuta
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
                $('#exampleModal').modal('show');
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
                                                        <div class="mb-1 col-lg-3 justify-content-end">
                                                            <button class="btn btn-custom">Visualizar</button>
                                                        </div>
                                                        <div class="mb-1 col-lg-3 justify-content-end">
                                                            <button class="btn btn-opuesto">Eliminar</button>
                                                        </div>
                                                    </div>
                                                    <hr>`
    })
}