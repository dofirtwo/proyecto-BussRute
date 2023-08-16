from django.urls import path
from . import views

urlpatterns = [
    path('ruta', views.RutaList.as_view()),
    path('ruta/<int:pk>', views.RutaDetail.as_view()),
    path('detalleRuta', views.DetalleRutaList.as_view()),
    path('detalleRuta/<int:pk>', views.DetalleRutaDetail.as_view()),
]