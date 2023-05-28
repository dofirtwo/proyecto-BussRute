from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request,"inicio.html")

def visualizarRutas(request):
    return render(request, "usuario/inicio.html")
