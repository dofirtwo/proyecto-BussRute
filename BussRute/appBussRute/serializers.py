from rest_framework import serializers
from appBussRute.models import Ruta,DetalleRuta

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