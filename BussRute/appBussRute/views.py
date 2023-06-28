from django.shortcuts import render, redirect
from django.db import Error, transaction
from appBussRute.models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import JsonResponse
from smtplib import SMTPException
import threading
import urllib
import random
import string


# Create your views here.
def inicio(request):
    return render(request,"inicio.html")

def crearCuenta(request):
    return render(request,"crearCuenta.html")

def visualizarRutas(request):
    return render(request, "usuario/inicio.html")
def comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentarios/comentarios.html', {'comentarios': comentarios})


def agregarComentario(request):
    if request.method == 'POST':
        if 'regresar' in request.POST:
            return redirect('/comentarios/')
        else:
            # Creamos un objeto de tipo comentario
            nombre = request.POST.get("txtNombre")
            comentario = request.POST.get("txtComentario")
            try:

                with transaction.atomic():
                    contenidoComentario = Comentario(nombre=nombre,
                                             comentario=comentario)
                    contenidoComentario.save()
                    mensaje = "Comentario registrado correctamente"
                    retorno = {"mensaje": mensaje}
                    return redirect("/comentarios/", retorno)
            except Error as error:
                transaction.rollback()
                mensaje = f"{error}"
                retorno = {"mensaje": mensaje, "comentario": contenidoComentario}
                return render(request, 'comentarios/agregarComentario.html')
    else:
        return render(request,'comentarios/agregarComentario.html')
    
def inicioSesion(request):
    return render(request,"inicioSesion.html")

def vistaRegistrarRuta(request):
    return render(request,"admin/frmRegistrarRuta.html")

def registroRuta(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = int(request.POST["numeroRuta"])
                horario = request.POST["horario"]
                empresa = request.POST["empresa"]
                ruta = Ruta(rutNumero=numeroRuta,rutHorario=horario,rutEmpresa=empresa)
                ruta.save()
                detalleRutas = json.loads(request.POST["detalle"])
                for detalle in detalleRutas:
                    latitud = detalle['latitud']               
                    longitud = detalle['longitud']
                    detalleRuta = DetalleRuta(detRuta=ruta,detLatitud=latitud,detLongitud=longitud)
                    detalleRuta.save()
                estado = True
                mensaje = "Se ha registrado la Solicitud Correctamete"
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":estado}
        return JsonResponse(retorno)
