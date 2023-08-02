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
from django.urls import path
from appBussRute import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/',views.inicio),
    path('', RedirectView.as_view(url='/inicio/')),
    path('visualizarRutas/',views.visualizarRutas),
    path('comentarios/', views.comentarios),
    path('agregarComentario/', views.agregarComentario),
    path('inicioSesion/',views.inicioSesion),
    path('vistaRegistrarRuta/',views.vistaRegistrarRuta),
    path('vistaRegistrarCuenta/', views.crearCuenta),
    path('registrarCuenta/',views.registrarseUsuario),
    path('iniciarSesion/', views.iniciarSesion),
    path('cerrarSesion/', views.cerrarSesion),
    path('vistaEnvioCorreo/',views.vistaEnvioCorreo),
    path('enviarCambioContrasena/',views.enviarCambioContrasena),
    path('vistaCambioContrasena/',views.vistaCambioContrasena),
    path('cambioContrasena/', views.cambiarContrasena),
    path('verificarSesion/', views.verificarSesion, name='verificarSesion'),
    path('registroRuta/', views.registroRuta),
    path('google-login/', views.google_login, name='google-login'),
    path('google-auth/', views.google_auth, name='google-auth'),
]
