function verificarSesion() {
  $.ajax({
    url: '/verificarSesion/',
    method: 'GET',
    success: function (data) {
      console.log(data)
      if (data.logueado) {
        // Si el usuario está logueado, lo redirigimos al formulario de comentarios.
        redirigir();
      } else {
        // Si el usuario no ha iniciado sesión, mostramos un mensaje de error.
        Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error').then(function () {
          setTimeout(function () {
            window.location.href = '/inicioSesion/';
          }, 500);
        });;
      }
    }
  });
}

//CODIGO COMENTARIOS Y CALIFICACION COMENTARIOS
function redirigir() {
  location.href = "/agregarComentario/"

}

$(document).ready(function() {
  const txtValoracion = $('#txtValoracion');
  let selectedCount = 0;

  $(document).on('click', '.heart', function() {
    const index = $('.heart').index(this);

    // Deseleccionar todos los corazones
    $('.heart').removeClass('selected');

    // Seleccionar corazones hasta el índice actual
    for (let i = 0; i <= index; i++) {
      $('.heart').eq(i).addClass('selected');
    }

    selectedCount = index + 1;

    // Actualizar la valoración basada en los corazones seleccionados
    txtValoracion.val(selectedCount);

    // Imprimir el valor en la consola
    console.log(`Valor del corazón: ${selectedCount}`);
  });

  $('#btnEnviar').on('click', function(e) {
    if (selectedCount === 0) {
      // Mostrar mensaje de SweetAlert2 si no se ha seleccionado ningún corazón
      e.preventDefault(); // Evita que el formulario se envíe
      Swal.fire("Dejanos tu calificación", "Eso nos ayudará a mejorar tu experiencia", "info");
    }
  });
});

function verFavoritos() {
  $.ajax({
    url: '/verificarSesion/',
    method: 'GET',
    success: function (data) {
      console.log(data)
      if (data.logueado) {
        // Si el usuario ha iniciado sesión, muestra el modal.
        $('#exampleModal').modal('show');
      } else {
        // Si el usuario no ha iniciado sesión, muestra un mensaje de error.
        Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error');
      }
    }
  });
}

function guardarRuta() {
  $.ajax({
    url: '/verificarSesion/',
    method: 'GET',
    success: function (data) {
      console.log(data)
      if (data.logueado) {
          Swal.fire('Cuenta', 'Ruta Agregada Correctamente', 'success');
      } else {
          Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error');
      }
    }
  });
}

$(function () {

  var app_id = '784661986686095';
  var scopes = 'email, public_profile';

  var btn_login = '<button type="submit" id="login" type="button" class="btn btn-outline-primary flex-grow-1 ml-2"><i class="fab fa-facebook-f lead mr-2"></i> Facebook</button>';

  var div_session = "<div id='facebook-session'>" +
    "<strong></strong>" +
    "<img>" +
    "<a href='#' id='logout' class='btn btn-danger'>Cerrar sesión</a>" +
    "</div>";

  window.fbAsyncInit = function () {

    FB.init({
      appId: app_id,
      status: true,
      cookie: true,
      xfbml: true,
      version: 'v17.0'
    });


    FB.getLoginStatus(function (response) {
      statusChangeCallback(response, function () { });
    });
  };

  var statusChangeCallback = function (response, callback) {
    console.log(response);

    if (response.status === 'connected') {
      getFacebookData();
    } else {
      callback(false);
    }
  }

  var checkLoginState = function (callback) {
    FB.getLoginStatus(function (response) {
      callback(response);
    });
  }

  var getFacebookData = function () {
    FB.api('/me', function (response) {
      $('#login').after(div_session);
      $('#login').remove();
      $('#facebook-session strong').text("Bienvenido: " + response.name);
      $('#facebook-session img').attr('src', 'http://graph.facebook.com/' + response.id + '/picture?type=large');
    });
  }

  var facebookLogin = function () {
    checkLoginState(function (data) {
      if (data.status !== 'connected') {
        FB.login(function (response) {
          if (response.status === 'connected')
            getFacebookData();
        }, { scope: scopes });
      }
    })
  }

  var facebookLogout = function () {
    checkLoginState(function (data) {
        console.log(data)
      if (data.status === 'connected') {
        FB.logout(function (response) {
            console.log(response)
          $('#facebook-session').before(btn_login);
          $('#facebook-session').remove();
        })
      }
    })

  }



  $(document).on('click', '#login', function (e) {
    e.preventDefault();

    facebookLogin();
  })

  $(document).on('click', '#logout', function (e) {
    e.preventDefault();

    if (confirm("¿Está seguro?"))
      facebookLogout();
    else
      return false;
  })

})

function a(){
  $(document).ready(function () {
      event.preventDefault();
      $('.dropdown-menu').toggle();
  });

}


function visualizarContraseña(inputId) {
  const mostrarContraseña = document.querySelector('#mostrarContraseña');
  const passwordInput = document.querySelector(`#${inputId}`);

  mostrarContraseña.addEventListener('click', function (e) {
    // Cambiar el tipo de entrada del campo de contraseña
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    // Cambiar el icono del botón
    this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
  });
}
visualizarContraseña('passwordUsuario');
visualizarContraseña('pasNuevaContraseña');

function resaltar(element) {
  element.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.5)";
}

function quitarResalte(element) {
  element.style.boxShadow = "none";
}