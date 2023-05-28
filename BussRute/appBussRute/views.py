from django.shortcuts import render, redirect
from django.db import Error, transaction
from appBussRute.models import Comentario

# Create your views here.
def inicio(request):
    return render(request,"inicio.html")

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
