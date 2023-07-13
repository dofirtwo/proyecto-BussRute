function redirigir() {
  location.href = "/agregarComentario/"
}

$(function () {

  var app_id = '784661986686095';
  var scopes = 'email, user_friends, user_online_presence';

  var btn_login = '<button id="login" type="button" class="btn btn-outline-primary flex-grow-1 ml-2"><i class="fab fa-facebook-f lead mr-2"></i> Facebook</button>';

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
      version: 'v2.1'
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
      if (data.status === 'connected') {
        FB.logout(function (response) {
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

$(document).ready(function() {
  $('#navbarDropdown').on('click', function(event) {
      event.preventDefault();
      $('.dropdown-menu').toggle();
  });
});

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