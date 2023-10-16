$(function () {
  //se utiliza para las peticiones ajax con query
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  $("#btnGuardar").click(function () {
    guardarRuta();
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

/**
 * Esta funcion se encarga de realizar la peticion para añadir una Ruta a Favoritos
 * y si sale correcto o hay error muestra una alerta
 */
function añadirFavorito() {
  if (document.getElementById("ruta").value == "") {
    Swal.fire('Ruta', 'Debe Seleccionar la Ruta Primero', 'error');
  } else {
    var datos = {
      "ruta": $("#ruta").val(),
    }
    $.ajax({
      url: "/registroFavorito/",
      data: datos,
      type: 'post',
      dataType: 'json',
      cache: false,
      success: function (resultado) {
        if (resultado.estado == false) {
          Swal.fire('Cuenta', resultado.mensaje, 'error');
        } else {
          Swal.fire('Cuenta', resultado.mensaje, 'success')
            .then((result) => {
              if (result.isConfirmed) {
                window.location.reload();
              }
            });

        }

      }
    })
  }
}

//CODIGO COMENTARIOS Y CALIFICACION COMENTARIOS
function redirigir() {
  location.href = "/agregarComentario/"

}

$(document).ready(function () {
  const txtValoracion = $('#txtValoracion');
  let selectedCount = 0;

  $(document).on('click', '.star', function () {
    const index = $('.star').index(this);

    // Deseleccionar todos los corazones
    $('.star').removeClass('selected');

    // Seleccionar corazones hasta el índice actual
    for (let i = 0; i <= index; i++) {
      $('.star').eq(i).addClass('selected');
    }

    selectedCount = index + 1;

    // Actualizar la valoración basada en los corazones seleccionados
    txtValoracion.val(selectedCount);

    // Imprimir el valor en la consola
    console.log(`Valor del star: ${selectedCount}`);
  });

  $('#btnEnviar').on('click', function (e) {
    if (selectedCount === 0) {
      // Mostrar mensaje de SweetAlert2 si no se ha seleccionado ningún corazón
      e.preventDefault(); // Evita que el formulario se envíe
      Swal.fire("Dejanos tu calificación", "Eso nos ayudará a mejorar tu experiencia", "info");
    }
  });
});

function eliminarComentario(idComentario) {
  Swal.fire({
    title: 'Eliminar Comentario',
    text: '¿Estás seguro de eliminar el Comentario?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    cancelButtonText: 'No',
    confirmButtonText: 'Sí'
  }).then((result) => {
    if (result.isConfirmed) {
      // Redirigir a la URL de eliminación
      location.href = `/eliminarComentario/${idComentario}/`;
    }
  });
}
//TERMINA COMENTARIOS SECCION

function guardarRuta() {
  $.ajax({
    url: '/verificarSesion/',
    method: 'GET',
    success: function (data) {
      if (data.logueado) {
        añadirFavorito()
      } else {
        Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error');
      }
    }
  });
}

function a() {
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

$(document).ready(function () {
  $('#passwordUsuario').on('input', function () {
    var password = $(this).val();
    var caracteres = /^(?=.*[0-9])(?=.*[a-zA-ZñÑ])([a-zA-Z0-9ñÑ\W_]+){8,}$/;

    if (!caracteres.test(password)) {
      $('#passwordError').text('La contraseña debe tener al menos 8 caracteres y contener letras y números.');
      $('#submitButton').prop('disabled', true);
    } else {
      $('#passwordError').text('');
      $('#submitButton').prop('disabled', false);
    }
  });

  $('#passwordUsuario').on('blur', function () {
    if ($(this).val() === '') {
      $('#passwordError').text('');
    }
    $('#mayusActivadaCrear').text('');
  });

  $('#passwordUsuario').keydown(function (e) {
    if (e.which === 20) {
      if ($('#mayusActivadaCrear').text() === '') {
        $('#mayusActivadaCrear').text('La tecla de mayúsculas está activada.');
      } else {
        $('#mayusActivadaCrear').text('');
      }
    }
  });
});


$(document).ready(function () {
  $('#pasNuevaContraseña').on('input', function () {
    var password = $(this).val();
    var caracteres = /^(?=.*[0-9])(?=.*[a-zA-ZñÑ])([a-zA-Z0-9ñÑ\W_]+){8,}$/;

    if (!caracteres.test(password)) {
      $('#passwordErrorCambio').text('La contraseña debe tener al menos 8 caracteres y contener letras y números.');
      $('#submitButtonCambio').prop('disabled', true);
    } else {
      $('#passwordErrorCambio').text('');
      $('#submitButtonCambio').prop('disabled', false);
    }
  });

  $('#pasNuevaContraseña').on('blur', function () {
    if ($(this).val() === '') {
      $('#passwordError').text('');
    }
    $('#mayusActivadaCambio').text('');
  });
  $('#pasNuevaContraseña').keydown(function (e) {
    if (e.which === 20) {
      if ($('#mayusActivadaCambio').text() === '') {
        $('#mayusActivadaCambio').text('La tecla de mayúsculas está activada.');
      } else {
        $('#mayusActivadaCambio').text('');
      }
    }
  });
});


