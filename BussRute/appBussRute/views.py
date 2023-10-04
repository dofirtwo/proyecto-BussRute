import requests
import matplotlib
matplotlib.use("Agg")  # Cambia el backend a uno no interactivo
import matplotlib.pyplot as plt
import json
from google.auth.transport import requests as google_requests
from django.shortcuts import render, redirect
from django import forms
from urllib.parse import urlencode
from django.db import Error, transaction
from appBussRute.models import *
from django.contrib.auth.models import *
from django.core.exceptions import ObjectDoesNotExist
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from smtplib import SMTPException
from datetime import datetime, timedelta, timezone
from google.oauth2 import id_token
from django.http import JsonResponse
import secrets
from django.core.validators import validate_email
from rest_framework import generics
from django.utils.crypto import get_random_string
from appBussRute.serializers import *
from cryptography.fernet import Fernet
import os
import random
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

# Generar una clave de cifrado
key = Fernet.generate_key()

# Convertir la clave de cifrado en una cadena y almacenarla en una variable de entorno
os.environ['ENCRYPTION_KEY'] = key.decode()

# BLOQUE DE SOLO VISTAS -------------------------------------------------------------------------------------------

def loginRequired(function):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' in request.session:
            # El usuario ya ha iniciado sesión, redirigirlo a otra página
            return redirect('/inicio/')
        else:
            # El usuario no ha iniciado sesión, permitirle acceder a la vista
            return function(request, *args, **kwargs)
    return wrapper

@loginRequired
def inicioSesion(request):
    mensajeError = request.session.pop('mensajeError', None)
    return render(request, 'inicioSesion.html', {'mensaje': mensajeError})

def vistaVerificarCorreo(request):
    # Verifica si la variable de sesión 'registro_completado' está presente y es True.
    if request.session.get('registro_completado'):
        return render(request, "verificacionCorreo.html")
    else:
        return redirect("/inicioSesion/")

def inicio(request):

    usuario_id = request.session.get('usuario_id')
    usuario = None

    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
    comentarios = Comentario.objects.all()
    context = {
        'comentarios': comentarios,
        'usuario': usuario
    }
    return render(request, 'inicio.html',context)

def crearCuenta(request):
    # Verifica si la variable de sesión 'registro_completado' está presente y es True.
    if request.session.get('registro_completado'):
        return redirect("/vistaVerificarCorreo/")
    else:
        return render(request, "crearCuenta.html")

def visualizarRutas(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)

    rutasFavoritas = FavoritoRuta.objects.filter(favUsuario=usuario_id)
    comentarios = Comentario.objects.all()
    barriosNeiva = barrios
    comunasNeiva = comunas
    sitiosNeiva = sitiosDeInteres
    lista_ordenada_barrios = sorted(barriosNeiva)
    lista_ordenada_sitios = sorted(sitiosNeiva)
    rutas = Ruta.objects.all()
    ubicaciones = UbicacionRuta.objects.all()
    coordenadas = DetalleRuta.objects.all()
    retorno = {"rutas":rutas,"coordenadas":coordenadas,"usuario": usuario,"comentarios":comentarios,"barriosNeiva":lista_ordenada_barrios,
               "comunasNeiva":comunasNeiva,"sitiosNeiva":lista_ordenada_sitios,"ubicaciones":ubicaciones,"rutasFavoritas":rutasFavoritas}

    return render(request, "usuario/inicio.html", retorno)

def vistaRegistrarRuta(request):
    # Verificar si el usuario está autenticado
    if 'usuario_id' not in request.session:
        # Si el usuario no está autenticado, redirigirlo a la página de inicio de sesión
        return redirect('/inicioSesion/')

    # Obtener el objeto Usuario del usuario autenticado
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    barriosNeiva = barrios
    comunasNeiva = comunas
    sitiosNeiva = sitiosDeInteres
    lista_ordenada_barrios = sorted(barriosNeiva)
    lista_ordenada_sitios = sorted(sitiosNeiva)
    retorno = {"barriosNeiva":lista_ordenada_barrios,"comunasNeiva":comunasNeiva,"sitiosNeiva":lista_ordenada_sitios,"usuario": usuario}

    # Verificar si el usuario tiene el rol de administrador
    if usuario.usuRol_id != 1:
        # Si el usuario no tiene el rol de administrador, redirigirlo a otra página
        return redirect('/inicio/')

    # Código para mostrar la vista para usuarios con rol de administrador
    return render(request, "admin/frmRegistrarRuta.html",retorno)

def vistaEnvioCorreo(request):
    return render(request, "contrasenaOlvidada.html")

def vistaNombreUsuario(request):
    # Leer la clave de cifrado de una variable de entorno y convertirla en un objeto de bytes
    key = os.environ['ENCRYPTION_KEY'].encode()
    # Crear una instancia de Fernet con la clave de cifrado
    f = Fernet(key)
    encrypted_email = request.GET.get('email', '')
    email = f.decrypt(encrypted_email.encode()).decode()
    return render(request, "nombreUsuario.html", {'email': email})

def generarCodigoVerificacion():
    return str(random.randint(100000, 999999))

clientID = '279970518458-chlpaq00krnoahgvdqdftdcfsu3gp8b9.apps.googleusercontent.com'
redirectUri = 'https://bussrute.pythonanywhere.com/google-auth/'

def contacto(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
    return render(request,'contacto.html', {'usuario':usuario})

# BLOQUE DE VARGAS FUNCIONES -------------------------------------------------------------------------------------------

def registroRuta(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = int(request.POST["numeroRuta"])
                precio = request.POST["precio"]
                empresa = request.POST["empresa"]
                ruta = Ruta(rutNumero=numeroRuta,rutPrecio=precio,rutEmpresa=empresa)
                ruta.save()
                detalleRutas = json.loads(request.POST["detalle"])
                for detalle in detalleRutas:
                    latitud = detalle['latitud']
                    longitud = detalle['longitud']
                    detalleRuta = DetalleRuta(detRuta=ruta,detLatitud=latitud,detLongitud=longitud)
                    detalleRuta.save()
                ubicacionRutas = json.loads(request.POST["ubicacion"])
                for ubicacion in ubicacionRutas:
                    barrio = ubicacion['barrio']
                    comuna = ubicacion['comuna']
                    sitioDeInteres = ubicacion['sitioDeInteres']
                    ubicacionRuta = UbicacionRuta(ubiRuta=ruta,ubiBarrio=barrio,ubiComuna=comuna,ubiSitioDeInteres=sitioDeInteres)
                    ubicacionRuta.save()
                estado = True
                mensaje = "Se ha registrado la Ruta Correctamente"
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":estado}
        return JsonResponse(retorno)

def eliminarFavorito(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = int(request.POST["numeroRuta"])
                ruta = Ruta.objects.get(rutNumero=numeroRuta)
                favorito = FavoritoRuta.objects.filter(favRuta=ruta)
                favorito.delete()
                mensaje="Ruta Favorita Eliminada"
        except Error as error:
            mensaje = f"problemas al eliminar {error}"

        retorno = {"mensaje":mensaje}
        return JsonResponse(retorno)

def listaRutas(request):
    try:
        usuario_id = request.session.get('usuario_id')
        usuario = None

        if usuario_id:
            usuario = Usuario.objects.get(id=usuario_id)
        rutas = Ruta.objects.all()
        mensaje=""
    except Error as error:
        mensaje = f"problemas al listar Productos {error}"
    retorno = {"mensaje":mensaje,"listaRutas":rutas,"usuario":usuario}
    return render (request, "admin/frmListaRutas.html",retorno)

def eliminarRuta(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                id = int(request.POST["id"])
                ruta = Ruta.objects.get(id=id)
                detalleRuta = DetalleRuta.objects.filter(detRuta=ruta)
                ubicacion = UbicacionRuta.objects.filter(ubiRuta=ruta)
                ubicacion.delete()
                detalleRuta.delete()
                ruta.delete()
                mensaje="Ruta Eliminada"
        except Error as error:
            mensaje = f"problemas al eliminar {error}"

        retorno = {"mensaje":mensaje}
        return JsonResponse(retorno)

def registroFavorito(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = request.POST["ruta"]
                print(f"numeroRuta: {numeroRuta}")  # Agrega esta línea

                if (numeroRuta==0):
                    mensaje="Debe Ingresar una Ruta Primero"
                else:
                    usuario_id = request.session.get('usuario_id')
                    print(f"usuario_id: {usuario_id}")
                    usuario = None
                    ruta = None
                    if usuario_id:
                        ruta = Ruta.objects.get(rutNumero=numeroRuta)
                        usuario = Usuario.objects.get(id=usuario_id)
                        rutFavorita = FavoritoRuta(favRuta=ruta,favUsuario=usuario)
                        rutFavorita.save()
                        mensaje="Ruta Añadida a Favorito Correctamente"
                    else:
                        mensaje="Debe Iniciar Sesion Primero"
                    estado = True
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":estado}
        return JsonResponse(retorno)



# BLOQUE DE ORTIZ Y CASTAÑEDA FUNCIONES -------------------------------------------------------------------------------------------

def agregarComentario(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)

    if 'usuario_id' not in request.session:
        # Si el usuario no está autenticado, redirigirlo a la página de inicio de sesión
        return redirect('/inicioSesion/')

    if request.method == 'POST':
        if 'regresar' in request.POST:
            return redirect('/inicio/')
        else:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = request.POST.get['txtComentario']
            # Creamos un objeto de tipo comentario
            nombre = request.POST.get("txtNombre")
            comentario = request.POST.get("txtComentario")
            valoracion = request.POST.get("txtValoracion")
            numRuta = request.POST.get("txtRuta")

            try:
                with transaction.atomic():
                    # Busca la instancia de Ruta correspondiente
                    if numRuta:
                        try:
                            ruta = Ruta.objects.get(rutNumero=numRuta)
                        except Ruta.DoesNotExist:
                            ruta = None
                    else:
                        ruta = None

                    # Crea un objeto de tipo Comentario con la ruta asociada
                    contenidoComentario = Comentario(comDescripcion=comentario, comUsuario_id=usuario_id, comValoracion=valoracion, comRuta=ruta)
                    contenidoComentario.save()
                    mensaje = "Comentario registrado correctamente"
                    retorno = {"mensaje": mensaje}
                    return redirect("/inicio/", retorno)

            except Error as error:
                transaction.rollback()
                mensaje = f"{error}"
                retorno = {"mensaje": mensaje,
                           "comentario": contenidoComentario}
                return render(request, 'comentarios/agregarComentario.html', retorno)
    else:
        # initial_data = {'txtNombre': request.user.username}
        # Obtener el nombre de usuario actual
        nombre_usuario = usuario.usuNombre if usuario else ''
        form = ComentarioForm(initial={'txtNombre': nombre_usuario})
        context = {'form': form, 'usuario': usuario}
        return render(request, 'comentarios/agregarComentario.html', context)

def eliminarComentario(request,id):
    try:
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
        mensaje="comentario eliminado"
    except Error as error:
        mensaje=f"problemas al eliminar el comentario {error}"

    retorno = {"mensaje": mensaje}

    return redirect("/inicio/",retorno)

def consultarComentario(request, id):
    usuario_id = request.session.get('usuario_id')
    usuario = None
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        try:
            comentario = Comentario.objects.get(id=id)
            mensaje=""
        except Error as error:
            mensaje = f"problemas {error}"
    retorno ={"mensaje":mensaje, "comentario":comentario, 'usuario':usuario}
    return render(request,"comentarios/frmEditarComentario.html", retorno)

def actualizarComentario(request, id):

    comDescripcion = request.POST["txtComentario"]
    comValoracion = int(request.POST["txtValoracion"])
    try:
        #actualizar el producto. PRIMERO SE CONSULTA
        comentario = Comentario.objects.get(id=id)
        comentario.comDescripcion=comDescripcion
        comentario.comValoracion=comValoracion
        comentario.save()
        mensaje="comentario actualizado correctamente"
        return redirect("/inicio/")
    except Error as error:
        mensaje = f"problemas al realizar el proceso de actualizar el comentario {error}"

    retorno = {"mensaje":mensaje,"comentario":comentario}
    return render(request,"frmEditar.html",retorno)



# BLOQUE DE CATAÑO FUNCIONES -------------------------------------------------------------------------------------------

def google_login(request):
    auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={clientID}&redirect_uri={redirectUri}&scope=email%20profile%20https://www.googleapis.com/auth/userinfo.profile%20openid&access_type=offline"
    return redirect(auth_url)

def google_auth(request):
    # Leer la clave de cifrado de una variable de entorno y convertirla en un objeto de bytes
    key = os.environ['ENCRYPTION_KEY'].encode()
    # Crear una instancia de Fernet con la clave de cifrado
    f = Fernet(key)
    if 'code' in request.GET:
        code = request.GET['code']
        print("codigo: ", code)
        data = {
            'code': code,
            'client_id': clientID,
            'client_secret': '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',
            'redirect_uri': redirectUri,
            'grant_type': 'authorization_code',
        }

        # Obtener el token de acceso con el código de autorización
        response = requests.post('https://accounts.google.com/o/oauth2/token', data=data)
        token_data = response.json()
        print("token de acceso:", token_data)

        if 'access_token' in token_data:
            idinfo = id_token.verify_oauth2_token(token_data['id_token'], google_requests.Request(), clientID)
            email = idinfo.get('email', None)
            print("Información del usuario obtenida")
            print(idinfo)

            try:
                # Verificar si el correo electrónico ya está registrado
                if Usuario.objects.filter(usuCorreo=email).exists():
                    # Si el correo electrónico ya está registrado, obtener el objeto Usuario
                    usuario = Usuario.objects.get(usuCorreo=email)
                    request.session['usuario_id'] = usuario.id
                    return redirect('/inicio/')
                else:
                    # Si el correo electrónico no está registrado, redirigir al usuario a la vista vistaNombreUsuario
                    encrypted_email = f.encrypt(email.encode()).decode()
                    return redirect(f'/vistaNombre/?email={encrypted_email}')

            except Exception as e:
                # Manejo de errores en caso de que algo falle en la creación o actualización del usuario
                print("Error:", e)

    return redirect('/inicio/')

def github_login(request):
    auth_params = {
        'client_id': settings.GITHUB_KEY,
        'scope': 'user:email',
    }
    auth_url = f'https://github.com/login/oauth/authorize?{urlencode(auth_params)}'
    return redirect(auth_url)

def github_callback(request):
    code = request.GET.get('code')
    key = os.environ['ENCRYPTION_KEY'].encode()
    # Crear una instancia de Fernet con la clave de cifrado
    f = Fernet(key)

    token_params = {
        'client_id': settings.GITHUB_KEY,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
    }

    token_headers = {'Accept': 'application/json'}
    token_response = requests.post('https://github.com/login/oauth/access_token', data=token_params, headers=token_headers)
    token_data = token_response.json()

    if 'access_token' in token_data:
        access_token = token_data['access_token']
        request.session['access_token'] = access_token

        user_headers = {'Authorization': f'token {access_token}'}
        user_response = requests.get('https://api.github.com/user', headers=user_headers)
        user_data = user_response.json()

        name = user_data['name']
        email = user_data.get('email')

        if email is None:
            mensaje = 'No podemos acceder a su correo electrónico. Es posible que esté en privado.'
            request.session['mensajeError'] = mensaje  # Almacenar el mensaje en la sesión
            return redirect('/inicioSesion/')  # Redirigir a la página inicioSesion

        try:
            # Verificar si el correo electrónico ya está registrado
            if Usuario.objects.filter(usuCorreo=email).exists():
                # Si el correo electrónico ya está registrado, obtener el objeto Usuario
                usuario = Usuario.objects.get(usuCorreo=email)
                request.session['usuario_id'] = usuario.id
                return redirect('/inicio/')
            else:
                # Si el correo electrónico no está registrado, redirigir al usuario a la vista vistaNombreUsuario
                encrypted_email = f.encrypt(email.encode()).decode()
                return redirect(f'/vistaNombre/?email={encrypted_email}')

        except Exception as e:
            # Manejo de errores en caso de que algo falle en la creación o actualización del usuario
            print("Error:", e)

    return redirect('/inicio/')

def desactivarOActivar(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                id = int(request.POST["id"])
                ruta = Ruta.objects.get(id=id)
                if ruta.rutEstado == 'A':
                    ruta.rutEstado = 'I'
                else:
                    ruta.rutEstado = 'A'
                ruta.save()
                mensaje = "Estado de la ruta actualizado"
        except Error as error:
            mensaje = f"Problemas al actualizar el estado {error}"

        retorno = {"mensaje": mensaje}
        return JsonResponse(retorno)

def verificarSesion(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        return JsonResponse({'logueado': True})
    else:
        return JsonResponse({'logueado': False})

def registrarseUsuario(request):
    try:
        nombreUsu = request.POST["nombreUsuario"]
        email = request.POST["correoUsuario"].lower()
        contrasena = request.POST["passwordUsuario"]

        # Verificar si el correo electrónico ya está registrado
        if Usuario.objects.filter(usuCorreo=email).exists():
            usuario = Usuario.objects.get(usuCorreo=email)
            if usuario.usuCreadoConGoogle:
                mensaje = "Inicia sesión con Google, ya que la cuenta fue creada utilizando este método de inicio de sesión"
                retorno = {"mensaje": mensaje, "estado": False}
                return render(request, "inicioSesion.html", retorno)
            else:
                mensaje = "Este correo ya se encuentra registrado."
                retorno = {"mensaje": mensaje, "estado": False}
                return render(request, "crearCuenta.html", retorno)
        elif len(nombreUsu) < 6:
            # Mostrar un mensaje de error al usuario
            mensaje = 'El nombre de usuario debe tener al menos 6 caracteres'
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "crearCuenta.html", retorno)

        if Usuario.objects.filter(usuNombre=nombreUsu).exists():
            mensaje = "El nombre de usuario ya está en uso. Por favor, elige otro."
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "crearCuenta.html", retorno)

        else:
            codigoDeVerificacion = generarCodigoVerificacion()
            request.session['nombreUsuario'] = nombreUsu
            request.session['correoUsuario'] = email
            request.session['contrasena'] = contrasena
            request.session['codigo_verificacion'] = codigoDeVerificacion
            request.session['registro_completado'] = True
            asunto = 'Verificacion del Correo Electronico'
            # Iniciar el hilo para enviar el correo electrónico
            mensaje = f'<div style="background:#f9f9f9">\
                            <div style="background-color:#f9f9f9">\
                                <div style="max-width:640px;margin:0 auto;border-radius:4px;overflow:hidden">\
                                    <div style="margin:0px auto;max-width:640px;background:#ffffff">\
                <table role="presentation" cellpadding="0" cellspacing="0"\
                    style="font-size:0px;width:100%;background:#ffffff" align="center" border="0">\
                    <tbody>\
                        <tr>\
                            <td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:40px 50px">\
                                <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                        <tbody>\
                                            <tr>\
                                                <td style="word-break:break-word;font-size:0px;padding:0px" align="center">\
                                                    <div style="color:#737f8d;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:16px;line-height:24px;text-align:center">\
                                                        <h2 style="font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-weight:500;font-size:20px;color:#4f545c;letter-spacing:0.27px">\
                                                            ¡Verificación de la Cuenta!</h2>\
                                                        <p>Confirma la cuenta con el siguiente\
                                                                código de\
                                                                confirmación.</p>\
                                                    </div>\
                                                </td>\
                                            </tr>\
                                            <tr>\
                                                <td style="word-break:break-word;font-size:0px;padding:10px 25px;padding-top:20px" align="center">\
                                                    <table role="presentation" cellpadding="0" cellspacing="0"\
                                                        style="border-collapse:separate" align="center" border="0">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td style="border:none;border-radius:3px;color:white;padding:15px 19px"\
                                                                    align="center" valign="middle"\
                                                                    bgcolor="#0077ff"><h2\
                                                                    style="text-decoration:none;line-height:100%;background:#0077ff;color:white;font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:15px;font-weight:normal;text-transform:none;margin:0px;letter-spacing:10px">\
                                                                    {codigoDeVerificacion}</h2>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </td>\
                                            </tr>\
                                            <tr>\
                                                <td bgcolor="#fff">\
                                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"\
                                                        bgcolor="#FFFFFF" style="border-top:1px solid #e2e2e2">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td\
                                                                    style="padding:30px 30px;text-align:center;font-family:"Roboto",sans-serif;font-size:15px;line-height:20px">\
                                                                    <table align="center" style="text-align:center">\
                                                                        <tbody>\
                                                                            <tr>\
                                                                                <td\
                                                                                    style="font-family:"Roboto",sans-serif;font-size:12px;line-height:20px;color:#555555;text-align:center;font-weight:300">\
                                                                                    <p class="m_-45816842390854781disclaimer"\
                                                                                        style="margin-bottom:5px">Este correo\
                                                                                        electrónico se envía para confirmar la dirección\
                                                                                        de correo electrónico que proporcionaste al\
                                                                                        crear tu cuenta en\
                                                                                        <span class="il">BussRute.</span>\
                                                                                        Si no solicitaste\
                                                                                        esta confirmación, Puedes ignorar este mensaje.\
                                                                                    </p>\
                                                                                </td>\
                                                                            </tr>\
                                                                        </tbody>\
                                                                    </table>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </td>\
                                            </tr>\
                                        </tbody>\
                                    </table>\
                                </div>\
                            </td>\
                        </tr>\
                    </tbody>\
                </table>\
            </div>\
        </div>\
        <div style="margin:0px auto;max-width:640px;background:transparent">\
            <table role="presentation" cellpadding="0" cellspacing="0"\
                style="font-size:0px;width:100%;background:transparent" align="center" border="0">\
                <tbody>\
                    <tr>\
                        <td\
                            style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:20px 0px">\
                            <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100"\
                                style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                    <tbody>\
                                        <tr>\
                                            <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                align="center">\
                                                <div\
                                                    style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                    Enviado por <span class="il">BussRute</span>\
                                                </div>\
                                            </td>\
                                        </tr>\
                                        <tr>\
                                            <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                align="center">\
                                                <div\
                                                    style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                    Derechos reservados: Ficha 2468288\
                                                </div>\
                                            </td>\
                                        </tr>\
                                    </tbody>\
                                </table>\
                            </div>\
                        </td>\
                    </tr>\
                </tbody>\
            </table>\
        </div>\
    </div>\
</div>'
            thread = threading.Thread(target=enviarCorreo,
                            args=(asunto, mensaje, [email], request))
            thread.start()
            thread.join()
            mensaje = f'Correo de verificación enviado.'
            retorno = {'mensaje': mensaje, 'estado': True}
            return render(request, "crearCuenta.html", retorno)
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
        retorno = {"mensaje": mensaje, "estado": False}

    return render(request, "crearCuenta.html", retorno)

def eliminarSesionRegistro(request):
    if 'registro_completado' in request.session:
        del request.session['registro_completado']
    if 'codigo_verificacion' in request.session:
        del request.session['codigo_verificacion']
    if 'nombreUsuario' in request.session:
        del request.session['nombreUsuario']
    if 'correoUsuario' in request.session:
        del request.session['correoUsuario']
    if 'contrasena' in request.session:
        del request.session['contrasena']

    return JsonResponse({'message': 'Sesión de registro eliminada'})

def verificarCodigoDeVerificacion(request):
    if request.method == "POST":
        codigoVerificacionIngresado = request.POST.get("codigoVerifi")

        # Obtiene el código de verificación almacenado en la variable de sesión
        codigoVerificacionGenerado = request.session.get('codigo_verificacion')

        if codigoVerificacionIngresado == codigoVerificacionGenerado:
            # Elimina el código de verificación de la variable de sesión
            del request.session['codigo_verificacion']
            del request.session['registro_completado']
            nombreUsuarioRe = request.session.get('nombreUsuario')
            correoUsuarioRe = request.session.get('correoUsuario')
            contrasena = request.session.get('contrasena')
            with transaction.atomic():
            # Buscar el rol "Usuario"
                rolUsuario = Rol.objects.get(id=2)

                user = Usuario(usuNombre=nombreUsuarioRe,
                           usuCorreo=correoUsuarioRe, usuRol=rolUsuario)
                # Almacenar la contraseña de forma segura
                user.set_password(contrasena)
                user.save()
                request.session['usuario_id'] = user.id
                mensaje = "El código de verificación es correcto. Tu cuenta ha sido verificada y se ha creado exitosamente."
                del request.session['nombreUsuario']
                del request.session['correoUsuario']
                del request.session['contrasena']
                retorno = {"mensaje": mensaje, "estado": True}
                return render(request, "verificacionCorreo.html", retorno)
        else:
            mensaje = "El código de verificación es incorrecto. Por favor, verifica nuevamente."
            estado = False

        return render(request, "verificacionCorreo.html", {"mensaje": mensaje, "estado": estado})

    return redirect("/inicio/")

def registrarUsuarioIniciadoGoogle(request):
    if request.method != 'POST':
        # Redirigir al usuario a otra página o mostrar un mensaje de error
        return redirect('/inicio/')
    try:
        nombreUsu = request.POST.get("nombreUsuarioGoogle","")
        email = request.POST.get("correoUsuarioGoogle","").lower()

        if not nombreUsu or not email:
            # Mostrar un mensaje de error al usuario
            mensaje = 'Por favor, complete todos los campos'
            retorno = {"mensaje": mensaje, "estado": False, "email": email}
            return render(request, "nombreUsuario.html", retorno)

        elif len(nombreUsu) < 6:
            # Mostrar un mensaje de error al usuario
            mensaje = 'El nombre de usuario debe tener al menos 6 caracteres'
            retorno = {"mensaje": mensaje, "estado": False, "email": email}
            return render(request, "nombreUsuario.html", retorno)

        elif Usuario.objects.filter(usuCorreo=email).exists():
            # Mostrar un mensaje de error al usuario
            mensaje = 'Ya existe una cuenta con este correo electrónico'
            retorno = {"mensaje": mensaje, "estado": False, "email": email}
            return render(request, "nombreUsuario.html", retorno)

        elif Usuario.objects.filter(usuNombre=nombreUsu).exists():
            mensaje = "El nombre de usuario ya está en uso. Por favor, elige otro."
            retorno = {"mensaje": mensaje, "estado": False, "email": email}
            return render(request, "nombreUsuario.html", retorno)

        else:
            with transaction.atomic():
                rolUsuario = Rol.objects.get(id=2)

            usuario = Usuario(
                usuNombre=nombreUsu,
                usuCorreo=email,
                usuRol=rolUsuario,
                usuCreadoConGoogle=True  # Indicar que la cuenta fue creada iniciando sesión con Google
            )
            usuario.set_password(get_random_string(10))
            usuario.save()

            request.session['usuario_id'] = usuario.id
            return redirect('/inicio/')

    except Error as error:
        transaction.rollback()
        mensaje = f"Ocurrió un error al intentar crear su cuenta: {error}"
        return render(request, "nombreUsuario.html", {'mensaje': mensaje})

def iniciarSesion(request):
    estado = False
    if request.method == 'POST':
        correo_o_usuario = request.POST['correoUsuarioInicioONombreUsuario'].lower()
        contrasena = request.POST['passwordUsuarioInicio']

        # Verificar si el valor ingresado es un correo electrónico válido
        try:
            validate_email(correo_o_usuario)
            # Si no se lanza una excepción, es un correo electrónico válido
            usuario = Usuario.objects.get(usuCorreo=correo_o_usuario)
        except ValidationError:
            # Si se lanza una excepción, no es un correo electrónico válido,
            # entonces asumimos que es el nombre de usuario
            try:
                usuario = Usuario.objects.get(usuNombre=correo_o_usuario)
            except Usuario.DoesNotExist:
                usuario = None

        if usuario:
            if usuario.usuCreadoConGoogle:
                # Si la cuenta fue creada iniciando sesión con Google, mostrar un mensaje al usuario
                mensaje = "Para acceder a tu cuenta, inicia sesión con Google, ya que la cuenta fue creada utilizando este método de inicio de sesión."
                return render(request, 'inicioSesion.html', {'mensaje': mensaje, 'estado': estado})
            else:
                # Si la cuenta no fue creada iniciando sesión con Google, continuar con el proceso de inicio de sesión
                if usuario.check_password(contrasena):
                    # Las credenciales son válidas
                    request.session['usuario_id'] = usuario.id
                    estado = True
                    response = redirect('/inicio/')  # Redirige al usuario a la página de inicio
                    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Evita el almacenamiento en caché
                    return response
                else:
                    mensaje = "La contraseña proporcionada es incorrecta."
        else:
            mensaje = "No hay una cuenta vinculada con el correo o nombre de usuario proporcionado."

        return render(request, 'inicioSesion.html', {'mensaje': mensaje, 'estado': estado})

    return render(request, 'inicioSesion.html', {'estado': estado})

def cerrarSesion(request):
    try:
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('/inicioSesion/')

@api_view(['POST'])
def enviarCorreoMovil(request):
    serializer = CorreoSerializer(data=request.data)
    if serializer.is_valid():
        correoUsuarioIngresado = serializer.validated_data['correoUsuarioIngresado']
        codigoVerificacionMovil = serializer.validated_data['codigoVerificacionMovil']
        asunto = 'Verificacion del Correo Electronico'
        mensaje = f'<div style="background:#f9f9f9">\
                            <div style="background-color:#f9f9f9">\
                                <div style="max-width:640px;margin:0 auto;border-radius:4px;overflow:hidden">\
                                    <div style="margin:0px auto;max-width:640px;background:#ffffff">\
                <table role="presentation" cellpadding="0" cellspacing="0"\
                    style="font-size:0px;width:100%;background:#ffffff" align="center" border="0">\
                    <tbody>\
                        <tr>\
                            <td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:40px 50px">\
                                <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                        <tbody>\
                                            <tr>\
                                                <td style="word-break:break-word;font-size:0px;padding:0px" align="center">\
                                                    <div style="color:#737f8d;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:16px;line-height:24px;text-align:center">\
                                                        <h2 style="font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-weight:500;font-size:20px;color:#4f545c;letter-spacing:0.27px">\
                                                            ¡Verificación de la Cuenta!</h2>\
                                                        <p>Confirma la cuenta con el siguiente\
                                                                código de\
                                                                confirmación.</p>\
                                                    </div>\
                                                </td>\
                                            </tr>\
                                            <tr>\
                                                <td style="word-break:break-word;font-size:0px;padding:10px 25px;padding-top:20px" align="center">\
                                                    <table role="presentation" cellpadding="0" cellspacing="0"\
                                                        style="border-collapse:separate" align="center" border="0">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td style="border:none;border-radius:3px;color:white;padding:15px 19px"\
                                                                    align="center" valign="middle"\
                                                                    bgcolor="#0077ff"><h2\
                                                                    style="text-decoration:none;line-height:100%;background:#0077ff;color:white;font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:15px;font-weight:normal;text-transform:none;margin:0px;letter-spacing:10px">\
                                                                    {codigoVerificacionMovil}</h2>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </td>\
                                            </tr>\
                                            <tr>\
                                                <td bgcolor="#fff">\
                                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"\
                                                        bgcolor="#FFFFFF" style="border-top:1px solid #e2e2e2">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td\
                                                                    style="padding:30px 30px;text-align:center;font-family:"Roboto",sans-serif;font-size:15px;line-height:20px">\
                                                                    <table align="center" style="text-align:center">\
                                                                        <tbody>\
                                                                            <tr>\
                                                                                <td\
                                                                                    style="font-family:"Roboto",sans-serif;font-size:12px;line-height:20px;color:#555555;text-align:center;font-weight:300">\
                                                                                    <p class="m_-45816842390854781disclaimer"\
                                                                                        style="margin-bottom:5px">Este correo\
                                                                                        electrónico se envía para confirmar la dirección\
                                                                                        de correo electrónico que proporcionaste al\
                                                                                        crear tu cuenta en\
                                                                                        <span class="il">BussRute.</span>\
                                                                                        Si no solicitaste\
                                                                                        esta confirmación, Puedes ignorar este mensaje.\
                                                                                    </p>\
                                                                                </td>\
                                                                            </tr>\
                                                                        </tbody>\
                                                                    </table>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </td>\
                                            </tr>\
                                        </tbody>\
                                    </table>\
                                </div>\
                            </td>\
                        </tr>\
                    </tbody>\
                </table>\
            </div>\
        </div>\
        <div style="margin:0px auto;max-width:640px;background:transparent">\
            <table role="presentation" cellpadding="0" cellspacing="0"\
                style="font-size:0px;width:100%;background:transparent" align="center" border="0">\
                <tbody>\
                    <tr>\
                        <td\
                            style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:20px 0px">\
                            <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100"\
                                style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                    <tbody>\
                                        <tr>\
                                            <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                align="center">\
                                                <div\
                                                    style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                    Enviado por <span class="il">BussRute</span>\
                                                </div>\
                                            </td>\
                                        </tr>\
                                        <tr>\
                                            <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                align="center">\
                                                <div\
                                                    style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                    Derechos reservados: Ficha 2468288\
                                                </div>\
                                            </td>\
                                        </tr>\
                                    </tbody>\
                                </table>\
                            </div>\
                        </td>\
                    </tr>\
                </tbody>\
            </table>\
        </div>\
    </div>\
</div>'
        correo = EmailMessage(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico almacenada en tus configuraciones
            [correoUsuarioIngresado],
        )
        correo.content_subtype = 'html'  # Aquí es donde especificas que el contenido del correo es HTML
        correo.send(fail_silently=False)

        return JsonResponse({'estado': 'Correo enviado correctamente'})
    else:
        return Response(serializer.errors, status=400)

def mostrarInterfaz(request, tokenCambio):
    try:
        user = Usuario.objects.get(usuTokenCambioContrasena=tokenCambio)
    except Usuario.DoesNotExist:
            estado = False
            mensaje = "Ya este token fue utilizado"
            retorno = {"mensaje": mensaje, "estado": estado}
            return render(request, "cambiarContraAndroid.html", retorno)

    return render(request, 'cambiarContraAndroid.html', {'tokenCambio': tokenCambio})

@api_view(['POST'])
def cambioAndroid(request):
    tokenCambio = request.POST.get('tokenCambio')
    pasNuevaContraseña = request.POST.get('androidNuevaContra')

    try:
        user = Usuario.objects.get(usuTokenCambioContrasena=tokenCambio)
    except Usuario.DoesNotExist:
            estado = False
            mensaje = "Ya este token fue utilizado"
            retorno = {"mensaje": mensaje, "estado": estado}
            return render(request, "cambiarContraAndroid.html", retorno)

    # Actualiza la contraseña del usuario y guarda el usuario
    user.set_password(pasNuevaContraseña)
    user.usuTokenCambioContrasena = None
    estado = True
    user.save()
    mensaje = "Contraseña cambiada correctamente"
    retorno = {"mensaje": mensaje, "estado": estado}
    return render(request, "cambiarContraAndroid.html", retorno)

@api_view(['POST'])
def enviarCorreoRecuperarContraseña(request):
    serializer = RecuperarContrasenaSerializer(data=request.data)
    if serializer.is_valid():
        correoCambio = serializer.validated_data['correoCambio']
        tokenCambio = serializer.validated_data['tokenCambio']
        try:
            user = Usuario.objects.get(usuCorreo=correoCambio)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=400)

        nombreUsuario = user.usuNombre
        user.usuTokenCambioContrasena = tokenCambio
        user.save()
        asunto = 'Solicitud para restablecer contraseña de BussRute'

        # Construye la URL de cambio de contraseña
        url = f"https://bussrute.pythonanywhere.com/enviarCorreoRecuperacion/{tokenCambio}"
        mensaje = f'<div style="background:#f9f9f9">\
                        <div style="background-color:#f9f9f9">\
                            <div style="max-width:640px;margin:0 auto;border-radius:4px;overflow:hidden">\
                                <div style="margin:0px auto;max-width:640px;background:#ffffff">\
                                    <table role="presentation" cellpadding="0" cellspacing="0"\
                                        style="font-size:0px;width:100%;background:#ffffff" align="center" border="0">\
                                        <tbody>\
                                            <tr>\
                                                <td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:40px 50px">\
                                                    <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                                        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                                            <tbody>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:0px" align="left">\
                                                                        <div style="color:#737f8d;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:16px;line-height:24px;text-align:left">\
                                                                            <h2 style="font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-weight:500;font-size:20px;color:#4f545c;letter-spacing:0.27px">\
                                                                                Hola, {nombreUsuario}:</h2>\
                                                                            <p>Haz clic en el siguiente botón para restablecer tu contraseña de <span class="il">BussRute</span>. Si no has solicitado una nueva contraseña, ignora este correo.</p>\
                                                                        </div>\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:10px 25px;padding-top:20px" align="center">\
                                                                        <table role="presentation" cellpadding="0" cellspacing="0"\
                                                                            style="border-collapse:separate" align="center" border="0">\
                                                                            <tbody>\
                                                                                <tr>\
                                                                                    <td style="border:none;border-radius:3px;color:white;padding:15px 19px"\
                                                                                        align="center" valign="middle"\
                                                                                        bgcolor="#0077ff"><a\
                                                                                            href="{url}"\
                                                                                            style="text-decoration:none;line-height:100%;background:#0077ff;color:white;font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:15px;font-weight:normal;text-transform:none;margin:0px">\
                                                                                            Restablecer contraseña\
                                                                                        </a></td>\
                                                                                </tr>\
                                                                            </tbody>\
                                                                        </table>\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:30px 0px">\
                                                                        <p\
                                                                            style="font-size:1px;margin:0px auto;border-top:1px solid #dcddde;width:100%">\
                                                                        </p>\
                                                                    </td>\
                                                                </tr>\
                                                            </tbody>\
                                                        </table>\
                                                    </div>\
                                                </td>\
                                            </tr>\
                                        </tbody>\
                                    </table>\
                                </div>\
                            </div>\
                            <div style="margin:0px auto;max-width:640px;background:transparent">\
                                <table role="presentation" cellpadding="0" cellspacing="0"\
                                    style="font-size:0px;width:100%;background:transparent" align="center" border="0">\
                                    <tbody>\
                                        <tr>\
                                            <td\
                                                style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:20px 0px">\
                                                <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100"\
                                                    style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                                    align="center">\
                                                                    <div\
                                                                        style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                                        Enviado por <span class="il">BussRute</span>\
                                                                    </div>\
                                                                </td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                                    align="center">\
                                                                    <div\
                                                                        style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                                        Derechos reservados: Ficha 2468288\
                                                                    </div>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </div>\
                                            </td>\
                                        </tr>\
                                    </tbody>\
                                </table>\
                            </div>\
                        </div>\
                    </div>'

        correo = EmailMessage(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico almacenada en tus configuraciones
            [correoCambio],
        )
        correo.content_subtype = 'html'  # Aquí es donde especificas que el contenido del correo es HTML
        correo.send(fail_silently=False)

        return JsonResponse({'estado': 'Correo de recuperacion enviado correctamente'})
    else:
        return Response(serializer.errors, status=400)

def enviarCorreo(asunto=None, mensaje=None, destinatario=None, request=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, destinatario)
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=False)
    except SMTPException as error:
        print(error)

def enviarCambioContrasena(request):
    try:
        correo = request.POST['recuCorreo']
        with transaction.atomic():
            if Usuario.objects.filter(usuCorreo=correo).exists():
                usuario = Usuario.objects.get(usuCorreo=correo)

                if usuario.usuCreadoConGoogle:
                    # Si la cuenta fue creada iniciando sesión con Google, mostrar un mensaje al usuario
                    mensaje = "No puedes solicitar un cambio de contraseña porque iniciaste sesión con Google."
                    retorno = {'mensaje': mensaje, 'estado': False}
                    return render(request, "contrasenaOlvidada.html", retorno)
                else:
                    # Generar token único
                    # Genera un token hexadecimal de 16 bytes
                    token = secrets.token_hex(16)

                    request.session['token'] = token

                    # Asignar el token al usuario
                    usuario.usuTokenCambioContrasena = token
                    usuario.save()

                    asunto = 'Solicitud para restablecer contraseña de BussRute'
                    #url = f"https://bussrute.pythonanywhere.com/vistaCambioContrasena/?token={token}"
                    url = f"http://127.0.0.1:8000/vistaCambioContrasena/?token={token}"
                    mensaje = f'<div style="background:#f9f9f9">\
                        <div style="background-color:#f9f9f9">\
                            <div style="max-width:640px;margin:0 auto;border-radius:4px;overflow:hidden">\
                                <div style="margin:0px auto;max-width:640px;background:#ffffff">\
                                    <table role="presentation" cellpadding="0" cellspacing="0"\
                                        style="font-size:0px;width:100%;background:#ffffff" align="center" border="0">\
                                        <tbody>\
                                            <tr>\
                                                <td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:40px 50px">\
                                                    <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                                        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                                            <tbody>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:0px" align="left">\
                                                                        <div style="color:#737f8d;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:16px;line-height:24px;text-align:left">\
                                                                            <h2 style="font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-weight:500;font-size:20px;color:#4f545c;letter-spacing:0.27px">\
                                                                                Hola, {usuario.usuNombre}:</h2>\
                                                                            <p>Haz clic en el siguiente botón para restablecer tu contraseña de <span class="il">BussRute</span>. Si no has solicitado una nueva contraseña, ignora este correo.</p>\
                                                                        </div>\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:10px 25px;padding-top:20px" align="center">\
                                                                        <table role="presentation" cellpadding="0" cellspacing="0"\
                                                                            style="border-collapse:separate" align="center" border="0">\
                                                                            <tbody>\
                                                                                <tr>\
                                                                                    <td style="border:none;border-radius:3px;color:white;padding:15px 19px"\
                                                                                        align="center" valign="middle"\
                                                                                        bgcolor="#0077ff"><a\
                                                                                            href="{url}"\
                                                                                            style="text-decoration:none;line-height:100%;background:#0077ff;color:white;font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:15px;font-weight:normal;text-transform:none;margin:0px">\
                                                                                            Restablecer contraseña\
                                                                                        </a></td>\
                                                                                </tr>\
                                                                            </tbody>\
                                                                        </table>\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td style="word-break:break-word;font-size:0px;padding:30px 0px">\
                                                                        <p\
                                                                            style="font-size:1px;margin:0px auto;border-top:1px solid #dcddde;width:100%">\
                                                                        </p>\
                                                                    </td>\
                                                                </tr>\
                                                            </tbody>\
                                                        </table>\
                                                    </div>\
                                                </td>\
                                            </tr>\
                                        </tbody>\
                                    </table>\
                                </div>\
                            </div>\
                            <div style="margin:0px auto;max-width:640px;background:transparent">\
                                <table role="presentation" cellpadding="0" cellspacing="0"\
                                    style="font-size:0px;width:100%;background:transparent" align="center" border="0">\
                                    <tbody>\
                                        <tr>\
                                            <td\
                                                style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:20px 0px">\
                                                <div aria-labelledby="mj-column-per-100" class="m_3451676835088794076mj-column-per-100"\
                                                    style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%">\
                                                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">\
                                                        <tbody>\
                                                            <tr>\
                                                                <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                                    align="center">\
                                                                    <div\
                                                                        style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                                        Enviado por <span class="il">BussRute</span>\
                                                                    </div>\
                                                                </td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td style="word-break:break-word;font-size:0px;padding:0px"\
                                                                    align="center">\
                                                                    <div\
                                                                        style="color:#99aab5;font-family:Helvetica Neue,Helvetica,Arial,Lucida Grande,sans-serif;font-size:12px;line-height:24px;text-align:center">\
                                                                        Derechos reservados: Ficha 2468288\
                                                                    </div>\
                                                                </td>\
                                                            </tr>\
                                                        </tbody>\
                                                    </table>\
                                                </div>\
                                            </td>\
                                        </tr>\
                                    </tbody>\
                                </table>\
                            </div>\
                        </div>\
                    </div>'

                    # Verificar si la dirección de correo electrónico es válida
                    try:
                        validate_email(correo)
                        # Iniciar el hilo para enviar el correo electrónico
                        thread = threading.Thread(target=enviarCorreo,
                                              args=(asunto, mensaje, [usuario.usuCorreo], request))
                        thread.start()
                        thread.join()
                        mensaje = f'Correo de recuperación enviado. Puede demorar unos minutos en llegar. Si no lo recibes, intenta enviarlo nuevamente.'
                        retorno = {'mensaje': mensaje, 'estado': True}
                        return render(request, "contrasenaOlvidada.html", retorno)
                    except ValidationError:
                        # Mostrar un mensaje de error si la dirección de correo electrónico no es válida
                        mensaje = f'Dirección de correo electrónico no válida'
            else:
                mensaje = f'Correo no se encuentra registrado'
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {'mensaje': mensaje, 'estado': False}
    return render(request, "contrasenaOlvidada.html", retorno)

def vistaCambioContrasena(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token is not None and tokenValido(token):
            # Token válido, permitir el cambio de contraseña
            return render(request, "cambiarContrasena.html")
        else:
            # Token inválido, mostrar un mensaje de error utilizando SweetAlert en la página "inicioSesion.html"
            mensaje = "No se ha solicitado un cambio de contraseña"
            request.session['mensajeError'] = mensaje
            return redirect('/inicioSesion/')

    # Manejar el caso si se realiza una solicitud POST para cambiar la contraseña
    elif request.method == 'POST':
        return cambiarContrasena(request,"cambiarContrasena.html")

def tokenValido(token):
    try:
        # Buscar el token en los usuarios
        usuario = Usuario.objects.get(usuTokenCambioContrasena=token)

        # Obtener la fecha y hora actual
        now = datetime.now(timezone.utc)

        # Obtener la fecha y hora límite de caducidad (10 minutos después de la generación del token)
        tiempoExpirar = usuario.fechaHoraActualizacion + timedelta(minutes=10)

        # Verificar si el tiempo actual está antes de la fecha de caducidad
        if now <= tiempoExpirar:
            return True
        else:
            return False

    except Usuario.DoesNotExist:
        return False

def cambiarContrasena(request):
    estado = False
    try:
        # Obtener el token de la sesión del usuario
        token = request.session.get('token')
        contraNueva = request.POST["pasNuevaContraseña"]
        usuario = Usuario.objects.get(usuTokenCambioContrasena=token)
        if tokenValido(token):
            usuario.set_password(contraNueva)
            usuario.usuTokenCambioContrasena = None
            usuario.save()
            estado = True
            mensaje = "Contraseña cambiada con éxito"
            del request.session['token']
        else:
            mensaje = "El token ha caducado o no es válido para cambiar la contraseña"
    except Usuario.DoesNotExist:
        mensaje = "No se encontró un usuario asociado a este token"
    except Error as error:
        mensaje = f"{error}"

    retorno = {"mensaje": mensaje, "estado": estado}
    return render(request, "cambiarContrasena.html", retorno)

def enviarMensajeContacto(request):
    nombreUsuario = request.POST.get('NombreUsuario')
    correoUsuario = request.POST.get('emailUsuario')
    asuntoUsuario = request.POST.get('asuntoUsuario')
    mensajeUsuario = request.POST.get('mensajeUsuario')
    try:
        thread = threading.Thread(target=enviarCorreoContacto,
                              args=(asuntoUsuario, mensajeUsuario, [settings.EMAIL_HOST_USER], correoUsuario, nombreUsuario, request))
        thread.start()
        thread.join()
        mensaje = f'Correo enviado exitosamente.'
        retorno = {'mensaje': mensaje, 'estado': True}
        return JsonResponse(retorno)
    except ValidationError:
        mensaje = f'No se pudo enviar el correo'
        
    return JsonResponse({'mensaje': mensaje, 'estado': False})

def enviarCorreoContacto(asunto=None, mensaje=None, destinatario=None, remitente=None, nombreUsuario=None, request=None):
    template = get_template('enviarCorreoContacto.html')
    print(remitente)
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
        'nombreUsuario': nombreUsuario  
    })
    try: 
        correo = EmailMultiAlternatives(
            asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=False)
    except SMTPException as error:
        print(error)



#------------------------------------------------------------------------------
def graficaEstadistica(request):
        # try:
        #     print(request.POST)
        #     color = '#960b0b'
        #     ruts = json.loads(request.POST("rutas"))
        #     ruta = []
        #     cantidad = []

        #     print(ruts)
        #     for rut in ruts:
        #         ruta.append(rut['ruta'])
        #         cantidad.append(rut['cantidad'])

        #     plt.title("PRODUCTOS MAS VENDIDOS")
        #     plt.xlabel("Productos")
        #     plt.ylabel("Ventas")


        #     # print(info)
        #     plt.bar(ruta, cantidad, color=color)
        #     imagen3 = os.path.join(settings.MEDIA_ROOT +"\\"+"grafica3.png")
        #     plt.savefig(imagen3)
        #     plt.tight_layout()
            return render(request, "admin/grafica.html")
        # except Error as error:
        #     mensaje = f"{error}"

# BLOQUE DE EN CASO DE CLASES -------------------------------------------------------------------------------------------

class ComentarioForm(forms.Form):
    txtNombre = forms.CharField(max_length=100)
    txtComentario = forms.CharField(widget=forms.Textarea)
    nombre_usuario = forms.CharField(widget=forms.HiddenInput)

# APIS ------------------------------------------------------------------------------------------------------------------

class RutaList(generics.ListCreateAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializers

class RutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializers
    lookup_field = 'rutNumero'

class RutaDetailAndroid(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializers

class FavoritoList(generics.ListCreateAPIView):
    queryset = FavoritoRuta.objects.all()
    serializer_class = FavoritoSerializers

class FavoritoDetailAndroid(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoritoRuta.objects.all()
    serializer_class = FavoritoSerializers
    lookup_field = 'favUsuario'

    def get_object(self):
        favUsuario = self.kwargs.get('favUsuario')
        favRuta = self.kwargs.get('favRuta')

        # Utiliza un filtro combinado para buscar por ambos campos
        obj = FavoritoRuta.objects.filter(favUsuario=favUsuario, favRuta=favRuta).first()


        return obj

class FavoritoDetail(generics.ListAPIView):  # Cambiamos RetrieveUpdateDestroyAPIView por ListAPIView
    serializer_class = FavoritoSerializers
    lookup_field = 'favUsuario'

    def get_queryset(self):
        favUsuario_value = self.kwargs[self.lookup_field]
        queryset = FavoritoRuta.objects.filter(favUsuario=favUsuario_value)
        return queryset

class DetalleRutaList(generics.ListCreateAPIView):
    queryset = DetalleRuta.objects.all()
    serializer_class = DetalleRutaSerializers

class DetalleRutaDetail(generics.ListAPIView):  # Cambiamos RetrieveUpdateDestroyAPIView por ListAPIView
    serializer_class = DetalleRutaSerializers
    lookup_field = 'detRuta'

    def get_queryset(self):
        detRuta_value = self.kwargs[self.lookup_field]
        queryset = DetalleRuta.objects.filter(detRuta=detRuta_value)
        return queryset

#PARTE DE USUARIO
class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsarioSerializers

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsarioSerializers

class RolList(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializers

#parte de comentarios
class ComentarioList(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

# Graficas---------------------------------------------------------------------------------
def get_data():
    # Obtiene los comentarios agrupados por ruta (excluyendo los que no tienen ruta)
    data_with_route = Comentario.objects.exclude(comRuta__isnull=True).values('comRuta__rutNumero').annotate(total=Count('comRuta')).order_by('-total')

    # Obtiene los comentarios que no tienen ruta
    data_without_route = Comentario.objects.filter(comRuta__isnull=True).count()

    # Prepara los datos para la gráfica
    labels = ['ruta:' + str(item['comRuta__rutNumero']) for item in data_with_route] + ['global']
    values = [item['total'] for item in data_with_route] + [data_without_route]

    return labels, values


def realizarGrafica(request):
    # Trae los datos de la base de datos
    labels, values = get_data()

    # Convierte las etiquetas a valores numéricos
    numeric_labels = range(len(labels))



    plt.subplot(2, 2, 1)
    # Añade títulos y etiquetas
    plt.title('Comentarios por Ruta')
    plt.xlabel('Ruta')
    plt.ylabel('Número de Comentarios')

    # Cambia las etiquetas del eje x a las etiquetas originales
    plt.xticks(numeric_labels, labels)
    # Crea la gráfica
    plt.bar(numeric_labels, values)
    #RUTAS GRAFICA
    ruta=[]
    for clave,valor in request.GET.items():
        ruta.append(valor)
    # Deserializar los elementos JSON y crear una nueva lista
    nueva_lista = [json.loads(item) if item.startswith('[') else item for item in ruta]

    # Inicializar una lista para las rutas
    ruta = []
    cantidad = []
    # Recorrer la nueva lista y agregar las rutas a la lista_de_rutas
    for item in nueva_lista:
        if isinstance(item, list):
            for sub_item in item:
                if isinstance(sub_item, str):
                    ruta.append(sub_item)
                elif isinstance(sub_item, int):
                    cantidad.append(sub_item)

    plt.subplot(2, 2, 2)
    plt.title("Rutas mas Usadas")
    plt.xlabel("Ruta")
    plt.ylabel("Cantidad")

    plt.bar(ruta,cantidad)

    grafica = os.path.join(settings.MEDIA_ROOT, "graficaRuta.png")
    plt.savefig(grafica)
    plt.tight_layout()

    mensaje= "Funcion"
    retorno = {'mensaje': mensaje, 'estado': False}
    return JsonResponse(retorno)

def verGraficas(request):
    return render(request,"admin/listaGrafica.html")

def get_data():
    # Obtiene los comentarios agrupados por ruta (excluyendo los que no tienen ruta)
    data_with_route = Comentario.objects.exclude(comRuta__isnull=True).values('comRuta__rutNumero').annotate(total=Count('comRuta')).order_by('-total')

    # Obtiene los comentarios que no tienen ruta
    data_without_route = Comentario.objects.filter(comRuta__isnull=True).count()

    # Prepara los datos para la gráfica
    labels = ['ruta:' + str(item['comRuta__rutNumero']) for item in data_with_route] + ['global']
    values = [item['total'] for item in data_with_route] + [data_without_route]

    return labels, values


def graficaComentario():
    # Trae los datos de la base de datos
    labels, values = get_data()

    # Convierte las etiquetas a valores numéricos
    numeric_labels = range(len(labels))

    # Crea la gráfica
    plt.bar(numeric_labels, values)

    # Añade títulos y etiquetas
    plt.title('Comentarios por Ruta')
    plt.xlabel('Ruta')
    plt.ylabel('Número de Comentarios')

    # Cambia las etiquetas del eje x a las etiquetas originales
    plt.xticks(numeric_labels, labels)

    # Guarda la gráfica en una imagen
    grafica = os.path.join(settings.MEDIA_ROOT, "graficaCom.png")
    plt.savefig(grafica)

    
graficaComentario()