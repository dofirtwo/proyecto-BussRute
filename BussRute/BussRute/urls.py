"""
URL configuration for BussRute project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appBussRute import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/',views.inicio),
    path('', RedirectView.as_view(url='/inicio/')),
    path('visualizarRutas/',views.visualizarRutas),
    #path('comentarios/', views.comentarios),
    path('listaRutas/', views.listaRutas),
    path('registroFavorito/',views.registroFavorito),
    path('eliminarFavorito/', views.eliminarFavorito),
    path('agregarComentario/', views.agregarComentario, name='agregarComentario'),
    path('inicioSesion/',views.inicioSesion),
    path('vistaRegistrarRuta/',views.vistaRegistrarRuta),
    path('vistaRegistrarCuenta/', views.crearCuenta),
    path('registrarCuenta/',views.registrarseUsuario),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('cerrarSesion/', views.cerrarSesion),
    path('iniciarSesion/', views.iniciarSesion),
    path('cerrarSesion/', views.cerrarSesion, name='cerrarSesion'),
    path('vistaEnvioCorreo/',views.vistaEnvioCorreo),
    path('enviarCambioContrasena/',views.enviarCambioContrasena),
    path('vistaCambioContrasena/',views.vistaCambioContrasena),
    path('cambioContrasena/', views.cambiarContrasena),
    path('verificarSesion/', views.verificarSesion, name='verificarSesion'),
    path('registroRuta/', views.registroRuta),
    path('vistaNombre/', views.vistaNombreUsuario),
    path('enviarNombreUsuario/', views.registrarUsuarioIniciadoGoogle, name='enviarNombreUsuario'),
    path('google-login/', views.google_login, name='google-login'),
    path('google-auth/', views.google_auth, name='google-auth'),
    path('github-login/', views.github_login, name='github-login'),
    path('github-auth/', views.github_callback, name='github-auth'),
    path('eliminarRuta/',views.eliminarRuta),
    path('eliminarComentario/<int:id>/',views.eliminarComentario, name='eliminarComentario'),
    path('consultarComentario/<int:id>/',views.consultarComentario, name='consultarComentario'),
    path('actualizarComentario/<int:id>/',views.actualizarComentario, name='actualizarComentario'),
    path('vistaVerificarCorreo/', views.vistaVerificarCorreo),
    path('enviarVerificacionCorreo/', views.verificarCodigoDeVerificacion),
    path('eliminarSesionRegistro/', views.eliminarSesionRegistro),
    path('realizarGrafica/', views.realizarGrafica),
    path('enviarCorreoRecuperacion/<str:tokenCambio>', views.mostrarInterfaz),
    path('cambioAndroid/', views.cambioAndroid),
    path('verGraficas/', views.verGraficas),
    path('vistaListaNuevo/', views.desactivarOActivar, name='desactivarOActivar'),
    path('contacto/', views.contacto),
    path("mensajeUsuario/", views.enviarMensajeContacto),
    path('', include('appBussRute.urls'))
]
