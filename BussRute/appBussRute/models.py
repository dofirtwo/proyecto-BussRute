from django.db import models

# Create your models here.

class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    comentario = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"