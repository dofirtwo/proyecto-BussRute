from django.db import models

# Create your models here.

class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    comentario = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"
    
class Ruta(models.Model):
    rutNumero = models.IntegerField(db_comment="Numero de la ruta del bus")
    rutHorario = models.TextField(db_comment="Hora aproximada en la que pasan los buses")
    rutEmpresa = models.TextField(db_comment="Id de Empresa")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def __str__(self):
        return f"{self.rutNumero}"
    
class DetalleRuta(models.Model):
    detRuta = models.ForeignKey(Ruta,on_delete=models.PROTECT,
                                    db_comment="Hace referencia a la ruta que se va a registrar")
    detLatitud = models.TextField(db_comment="Latitud de la trayectoria de la ruta")
    detLongitud = models.TextField(db_comment="Longitud de la trayectoria de la ruta")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self)->str:
        return f"{self.detLatitud}->{self.detLongitud}"