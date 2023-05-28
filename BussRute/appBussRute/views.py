from django.shortcuts import render
# Create your views here.
def inicio(request):
    return render(request,"inicio.html")

def inicioSesion(request):
    return render(request,"inicioSesion.html")