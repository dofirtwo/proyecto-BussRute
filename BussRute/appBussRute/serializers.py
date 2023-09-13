from rest_framework import serializers
from appBussRute.models import Ruta, DetalleRuta, Usuario, Rol
from appBussRute.models import Comentario

class RutaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ('id','rutNumero','rutHorario','rutEmpresa')

class DetalleRutaSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetalleRuta
        fields = ('id','detRuta','detLatitud','detLongitud')

#class ProductoSerializers(serializers.ModelSerializer):
#    class Meta:
#        model = Producto
#        fields = ('id','proCodigo','proNombre','proPrecio','proCategoria','proFoto')

class UsarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'usuNombre','usuCorreo', 'usuPassword', 'usuCreadoConGoogle','usuTokenCambioContrasena','usuRol')

class RolSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'rolNombre')
#Comentario
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id', 'comDescripcion', 'comValoracion', 'comUsuario')

class CorreoSerializer(serializers.Serializer):
    correoUsuarioIngresado = serializers.EmailField()
    codigoVerificacionMovil = serializers.CharField(max_length=6)

class RecuperarContrasenaSerializer(serializers.Serializer):
    correoCambio = serializers.EmailField()
    tokenCambio = serializers.CharField(max_length=16)