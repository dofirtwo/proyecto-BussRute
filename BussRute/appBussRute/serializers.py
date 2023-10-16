from rest_framework import serializers
from appBussRute.models import Ruta, DetalleRuta, Usuario, Rol,FavoritoRuta,UbicacionRuta
from appBussRute.models import Comentario

class RutaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ('id','rutNumero','rutPrecio','rutEmpresa')

class FavoritoSerializers(serializers.ModelSerializer):
    class Meta:
        model = FavoritoRuta
        fields = ('id','favRuta','favUsuario')

class UbicacionRutaSerializers(serializers.ModelSerializer):
    class Meta:
        model = UbicacionRuta
        fields = ('id','ubiRuta','ubiBarrio','ubiComuna','ubiSitioDeInteres')

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
        fields = ('id', 'comDescripcion', 'comValoracion', 'comUsuario', 'comRuta')

class CorreoSerializer(serializers.Serializer):
    correoUsuarioIngresado = serializers.EmailField()
    codigoVerificacionMovil = serializers.CharField(max_length=6)

class RecuperarContrasenaSerializer(serializers.Serializer):
    correoCambio = serializers.EmailField()
    tokenCambio = serializers.CharField(max_length=32)