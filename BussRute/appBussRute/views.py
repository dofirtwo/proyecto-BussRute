import requests
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
from appBussRute.serializers import RutaSerializers,DetalleRutaSerializers, UsarioSerializers, RolSerializers, ComentarioSerializer
from cryptography.fernet import Fernet
import os

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
    return render(request, "crearCuenta.html")

def visualizarRutas(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)

    rutasFavoritas = FavoritoRuta.objects.filter(favUsuario=usuario_id)
    barriosNeiva = barrios
    comunasNeiva = comunas
    sitiosNeiva = sitiosDeInteres
    lista_ordenada_barrios = sorted(barriosNeiva)
    lista_ordenada_sitios = sorted(sitiosNeiva)
    rutas = Ruta.objects.all()
    ubicaciones = UbicacionRuta.objects.all()
    coordenadas = DetalleRuta.objects.all()
    retorno = {"rutas":rutas,"coordenadas":coordenadas,"usuario": usuario,"barriosNeiva":lista_ordenada_barrios,
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

def registroFavorito(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = request.POST["ruta"]
                usuario_id = request.session.get('usuario_id')
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

def vistaEnvioCorreo(request):
    return render(request, "contrasenaOlvidada.html")

"""
def comentarios(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        comentarios = Comentario.objects.all()
        context = {
            'comentarios': comentarios,
            'usuario': usuario
        }
    return render(request, 'comentarios/comentarios.html', context)
"""


def vistaNombreUsuario(request):
    # Leer la clave de cifrado de una variable de entorno y convertirla en un objeto de bytes
    key = os.environ['ENCRYPTION_KEY'].encode()
    # Crear una instancia de Fernet con la clave de cifrado
    f = Fernet(key)
    encrypted_email = request.GET.get('email', '')
    email = f.decrypt(encrypted_email.encode()).decode()
    return render(request, "nombreUsuario.html", {'email': email})

# BLOQUE DE SOLO FUNCIONES -------------------------------------------------------------------------------------------

clientID = '279970518458-chlpaq00krnoahgvdqdftdcfsu3gp8b9.apps.googleusercontent.com'
redirectUri = 'https://bussrute.pythonanywhere.com/google-auth/'

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


def eliminarFavorito(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                numeroRuta = int(request.POST["numeroRuta"])
                ruta = Ruta.objects.get(rutNumero=numeroRuta)
                favorito = FavoritoRuta.objects.filter(favRuta=ruta)
                favorito.delete()
                mensaje="ProductoEliminado"
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
                ubicacion = UbicacionRuta.objects.get(ubiRuta=ruta)
                ubicacion.delete()
                detalleRuta.delete()
                ruta.delete()
                mensaje="Ruta Eliminada"
        except Error as error:
            mensaje = f"problemas al eliminar {error}"

        retorno = {"mensaje":mensaje}
        return JsonResponse(retorno)

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
                mensaje = "Se ha registrado la Ruta Correctamete"
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje":mensaje,"estado":estado}
        return JsonResponse(retorno)

def verificarSesion(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        return JsonResponse({'logueado': True})
    else:
        return JsonResponse({'logueado': False})

def agregarComentario(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)

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

        with transaction.atomic():
            # Buscar el rol "Usuario"
            rolUsuario = Rol.objects.get(id=1)

            user = Usuario(usuNombre=nombreUsu,
                           usuCorreo=email, usuRol=rolUsuario)
            # Almacenar la contraseña de forma segura
            user.set_password(contrasena)
            user.save()
            request.session['usuario_id'] = user.id
            mensaje = "Registrado correctamente"
            retorno = {"mensaje": mensaje, "estado": True}
            return render(request, "crearCuenta.html", retorno)

    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
        retorno = {"mensaje": mensaje, "estado": False}

    return render(request, "crearCuenta.html", retorno)

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
        correo = request.POST['correoUsuarioInicio'].lower()
        contrasena = request.POST['passwordUsuarioInicio']

        try:
            usuario = Usuario.objects.get(usuCorreo=correo)

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
        except ObjectDoesNotExist:
            mensaje = "No hay una cuenta vinculada con el correo proporcionado."

        return render(request, 'inicioSesion.html', {'mensaje': mensaje, 'estado': estado})

    return render(request, 'inicioSesion.html', {'estado': estado})

def cerrarSesion(request):
    try:
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('/inicioSesion/')

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

                    # Asignar el token al usuario
                    usuario.usuTokenCambioContrasena = token
                    usuario.save()

                    asunto = 'Solicitud para restablecer contraseña de BussRute'
                    #url = f"https://bussrute.pythonanywhere.com/vistaCambioContrasena/?token={token}&correo={correo}"
                    url = f"http://127.0.0.1:8000//vistaCambioContrasena/?token={token}&correo={correo}"
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
        correo = request.GET.get('correo')
        if token is not None and tokenValido(token, correo):
            # Token válido, permitir el cambio de contraseña
            return render(request, "cambiarContrasena.html", {"correo": correo})
        else:
            # Token inválido, mostrar un mensaje de error utilizando SweetAlert en la página "inicioSesion.html"
            mensaje = "No se ha solicitado un cambio de contraseña"
            request.session['mensajeError'] = mensaje
            return redirect('/inicioSesion/')

    # Manejar el caso si se realiza una solicitud POST para cambiar la contraseña
    elif request.method == 'POST':
        return cambiarContrasena(request, {"correo": correo})

def tokenValido(token, correo):
    try:
        # Buscar el token en los usuarios
        usuario = Usuario.objects.get(usuTokenCambioContrasena=token, usuCorreo = correo)

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
        contraNueva = request.POST["pasNuevaContraseña"]
        correo = request.POST.get('correo')
        usuario = Usuario.objects.get(usuCorreo=correo)
        usuario.set_password(contraNueva)
        # Limpiar el token después de cambiar la contraseña
        usuario.usuTokenCambioContrasena = None
        usuario.save()
        estado = True
        mensaje = "Contraseña cambiada con éxito"
    except Error as error:
        mensaje = f"{error}"

    retorno = {"mensaje": mensaje, "estado": estado}
    return render(request, "cambiarContrasena.html", retorno)

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

class DetalleRutaList(generics.ListCreateAPIView):
    queryset = DetalleRuta.objects.all()
    serializer_class = DetalleRutaSerializers

class DetalleRutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleRuta.objects.all()
    serializer_class = DetalleRutaSerializers
    lookup_field = 'detRuta'

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
