from rest_framework import serializers
from appBussRute.models import Ruta,DetalleRuta
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

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id', 'comDescripcion', 'comValoracion', 'comUsuario')
        
        