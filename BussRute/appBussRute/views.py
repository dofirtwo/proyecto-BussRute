import json
from django.shortcuts import render, redirect
from .models import Comentario
from django import forms
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


def verificarSesion(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        return JsonResponse({'logueado': True})
    else:
        return JsonResponse({'logueado': False})

# Create your views here.
def inicio(request):
    usuario = None
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'inicio.html', {'usuario': usuario})


def crearCuenta(request):
    return render(request, "crearCuenta.html")


def visualizarRutas(request):
    usuario_id = request.session.get('usuario_id')
    usuario = None

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        rutas = Ruta.objects.all()
        coordenadas = DetalleRuta.objects.all()
        retorno = {"rutas":rutas,"coordenadas":coordenadas}
        return render(request, "usuario/inicio.html", retorno)


    return render(request, "usuario/inicio.html", {'usuario': usuario})


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


class ComentarioForm(forms.Form):
    txtNombre = forms.CharField(max_length=100)
    txtComentario = forms.CharField(widget=forms.Textarea)
    nombre_usuario = forms.CharField(widget=forms.HiddenInput)


def agregarComentario(request):
        usuario_id = request.session.get('usuario_id')
        usuario = None
        if usuario_id:
            usuario = Usuario.objects.get(id=usuario_id)
            
        if request.method == 'POST':
            if 'regresar' in request.POST:
                return redirect('/comentarios/')
            else:
                form = ComentarioForm(request.POST)
                if form.is_valid():
                    comentario = request.POST.get['txtComentario']
                     
                 # Creamos un objeto de tipo comentario
                nombre = request.POST.get("txtNombre")
                comentario = request.POST.get("txtComentario")
                
                try:
                    with transaction.atomic():
                        contenidoComentario = Comentario(comDescripcion=comentario, comUsuario_id=usuario_id)
                        contenidoComentario.save()
                        mensaje = "Comentario registrado correctamente"
                        retorno = {"mensaje": mensaje}
                        return redirect("/comentarios/", retorno)
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


def inicioSesion(request):
    mensajeError = request.session.pop('mensajeError', None)
    return render(request, 'inicioSesion.html', {'mensaje': mensajeError})


def vistaRegistrarRuta(request):
    return render(request, "admin/frmRegistrarRuta.html")

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


def registrarseUsuario(request):
    try:
        nombreUsu = request.POST["nombreUsuario"]
        email = request.POST["correoUsuario"].lower()
        contraseña = request.POST["passwordUsuario"]

        # Verificar si el correo electrónico ya está registrado
        if Usuario.objects.filter(usuCorreo=email).exists():
            mensaje = "Este correo ya se encuentra registrado."
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "crearCuenta.html", retorno)

        with transaction.atomic():
            # Buscar el rol "Usuario"
            rolUsuario = Rol.objects.get(id=2)

            user = Usuario(usuNombre=nombreUsu,
                           usuCorreo=email, usuRol=rolUsuario)
            # Almacenar la contraseña de forma segura
            user.set_password(contraseña)
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


def iniciarSesion(request):
    estado = False
    if request.method == 'POST':
        correo = request.POST['correoUsuarioInicio'].lower()
        contraseña = request.POST['passwordUsuarioInicio']

        try:
            usuario = Usuario.objects.get(usuCorreo=correo)
            if usuario.check_password(contraseña):
                # Las credenciales son válidas
                request.session['usuario_id'] = usuario.id
                estado = True
                return redirect('/inicio/')
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


def vistaEnvioCorreo(request):
    return render(request, "contraseñaOlvidada.html")


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
        request.session['correo'] = destinatario[0]
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)


def enviarCambioContraseña(request):
    try:
        correo = request.POST['recuCorreo']
        with transaction.atomic():
            if Usuario.objects.filter(usuCorreo=correo).exists():
                usuario = Usuario.objects.get(usuCorreo=correo)
                # Generar token único
                # Genera un token hexadecimal de 16 bytes
                token = secrets.token_hex(16)

                # Asignar el token al usuario
                usuario.usuTokenCambioContraseña = token
                usuario.save()

                asunto = 'Solicitud para restablecer contraseña de BussRute'
                url = f"http://127.0.0.1:8000/vistaCambioContraseña/?token={token}"
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

                thread = threading.Thread(target=enviarCorreo,
                                          args=(asunto, mensaje, [usuario.usuCorreo], request))
                thread.start()
                print(mensaje)
                mensaje = f'Correo enviado correctamente'
                retorno = {'mensaje': mensaje, 'estado': True}
                return render(request, "contraseñaOlvidada.html", retorno)
            else:
                mensaje = f'Correo no se encuentra registrado'
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {'mensaje': mensaje, 'estado': False}
    return render(request, "contraseñaOlvidada.html", retorno)


def vistaCambioContraseña(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token is not None and tokenValido(token):
            # Token válido, permitir el cambio de contraseña
            return render(request, "cambiarContraseña.html")
        else:
            # Token inválido, mostrar un mensaje de error utilizando SweetAlert en la página "inicioSesion.html"
            mensaje = "No se ha solicitado un cambio de contraseña"
            request.session['mensajeError'] = mensaje
            return redirect('/inicioSesion/')

    # Manejar el caso si se realiza una solicitud POST para cambiar la contraseña
    elif request.method == 'POST':
        return cambiarContraseña(request)


def tokenValido(token):
    try:
        # Buscar el token en los usuarios
        usuario = Usuario.objects.get(usuTokenCambioContraseña=token)

        # Obtener la fecha y hora actual
        now = datetime.now(timezone.utc)

        # Obtener la fecha y hora límite de caducidad (10 minutos después de la generación del token)
        tiempoExpirar = usuario.fechaHoraActualizacion + timedelta(minutes=10)

        # Verificar si el tiempo actual está antes de la fecha de caducidad
        print(f"Token: {token}")
        print(f"Now: {now}")
        print(f"tiempoExpirar: {tiempoExpirar}")
        if now < tiempoExpirar:
            return True
        else:
            return False

    except Usuario.DoesNotExist:
        return False


def cambiarContraseña(request):
    estado = False
    try:
        contraNueva = request.POST["pasNuevaContraseña"]
        correo = request.session.get('correo')
        usuario = Usuario.objects.get(usuCorreo=correo)
        usuario.set_password(contraNueva)
        # Limpiar el token después de cambiar la contraseña
        usuario.usuTokenCambioContraseña = None
        usuario.save()
        estado = True
        mensaje = "Contraseña cambiada con éxito"
    except Error as error:
        mensaje = f"{error}"

    retorno = {"mensaje": mensaje, "estado": estado}
    return render(request, "cambiarContraseña.html", retorno)

