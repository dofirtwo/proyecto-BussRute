$(function(){
  //se utiliza para las peticiones ajax con query
  $.ajaxSetup({
      headers:{
          'X-CSRFToken':getCookie('csrftoken')
      }
  })
  $("#btnGuardar").click(function(){
    guardarRuta();
  })
})

function getCookie(name){
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0,name.length + 1) === (name + '=')){
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

function añadirFavorito(){
  var datos = {
    "ruta": $("#ruta").val(),
  }
  $.ajax({
      url: "/registroFavorito/",
      data: datos,
      type: 'post',
      dataType: 'json',
      cache: false,
      success: function(resultado){
          console.log(resultado);
      }
  })
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
          Swal.fire('Cuenta', 'Ruta Agregada Correctamente', 'success');
          window.location.reload();
      } else {
          Swal.fire('Cuenta', 'Debes iniciar sesión primero.', 'error');
      }
    }
  });
}

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


