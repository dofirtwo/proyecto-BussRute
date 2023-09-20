from django.urls import path
from . import views

urlpatterns = [
    path('ruta', views.RutaList.as_view()),
    path('ruta/<int:rutNumero>', views.RutaDetail.as_view()),
    path('rutaAndroid/<int:pk>', views.RutaDetailAndroid.as_view()),
    path('detalleRuta', views.DetalleRutaList.as_view()),
    path('detalleRuta/<int:detRuta>', views.DetalleRutaDetail.as_view()),
    path('favorito', views.FavoritoList.as_view()),
    path('favorito/<int:favUsuario>', views.FavoritoDetail.as_view()),
    path('favoritoAndroid/<int:favUsuario>/<int:favRuta>', views.FavoritoDetailAndroid.as_view()),
    #USUARIO
    path('usuario', views.UsuarioList.as_view()),
    path('usuario/<int:pk>', views.UsuarioDetail.as_view()), #el parametro no es de la cuenta de Google, si no el usuario creado con el id especifico
    path('rol', views.RolList.as_view()),
    #Comentario
    path('comentario', views.ComentarioList.as_view()),
    path('comentario/<int:pk>', views.ComentarioDetail.as_view()),
    path('enviarCorreoMovil/', views.enviarCorreoMovil),
    path('enviarCorreoRecuperacion/', views.enviarCorreoRecuperarContraseña),
]