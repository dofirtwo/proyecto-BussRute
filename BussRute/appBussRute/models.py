from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Rol(models.Model):
    rolNombre = models.CharField(max_length=50)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rolNombre}"

class Usuario(models.Model):
    usuNombre = models.CharField(max_length=21)
    usuCorreo = models.CharField(max_length=50)
    usuPassword = models.CharField(max_length=128)  # Almacenar la contraseña en un campo de longitud suficiente
    usuTokenCambioContrasena = models.CharField(max_length=50, null=True, blank=True)
    usuRol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def set_password(self, password):
        self.usuPassword = make_password(password)

    def check_password(self, password):
        return check_password(password, self.usuPassword)

    def __str__(self):
        return f"{self.usuNombre}"

class Comentario(models.Model):
    comDescripcion = models.CharField(max_length=100)
    comValoracion = models.CharField(max_length=30, null=True)
    comUsuario = models.ForeignKey(Usuario,on_delete=models.PROTECT, null=True)
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comDescripcion} + {self.comValoracion}"

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
