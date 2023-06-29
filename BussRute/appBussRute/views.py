from django.shortcuts import render, redirect
from django.db import Error, transaction
from appBussRute.models import *
from django.contrib.auth.models import *
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def inicio(request):
    usuario = None
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'inicio.html', {'usuario': usuario})


def crearCuenta(request):
    return render(request,"crearCuenta.html")

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
                                             comDescripcion=comentario)
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

def registrarseUsuario(request):
    try:
        nombreUsu = request.POST["nombreUsuario"]
        email = request.POST["correoUsuario"]
        contraseña = request.POST["passwordUsuario"]
        
        # Verificar si el correo electrónico ya está registrado
        if Usuario.objects.filter(usuCorreo=email).exists():
            mensaje = "Este correo ya se encuentra registrado."
            retorno = {"mensaje": mensaje, "estado": False}
            return render(request, "crearCuenta.html", retorno)
            
        with transaction.atomic():
            # Buscar el rol "Usuario"
            rolUsuario = Rol.objects.get(id=2)
            
            user = Usuario(usuNombre=nombreUsu, usuCorreo=email, usuRol=rolUsuario)
            user.set_password(contraseña)  # Almacenar la contraseña de forma segura
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
        correo = request.POST['correoUsuarioInicio']
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

