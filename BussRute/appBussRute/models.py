from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
import hashlib

# Create your models here.

barrios = [('Calamari', 'Calamari'),('Villa Marcela', 'Villa Marcela'),
           ('Asentamiento Villa Nazar', 'Asentamiento Villa Nazareth'),
           ('El Progreso', 'El Progreso'),('Dario Echandía', 'Dario Echandía'),
           ('Sector Pacolandia', 'Sector Pacolandia'),('Luis Ignacio Andrade', 'Luis Ignacio Andrade'),
           ('Vicente Araujo', 'Vicente Araujo'),('Santa Rosa', 'Santa Rosa'),('Eduardo Santos', 'Eduardo Santos'),
           ('Luis Eduardo Vanegas', 'Luis Eduardo Vanegas'),
           ('Luis Carlos Galán Sarmiento', 'Luis Carlos Galán Sarmiento'),('Alberto Galindo', 'Alberto Galindo'),
           ('Virgilio Barco', 'Virgilio Barco'),('Zona Sin Desarrollar', 'Zona Sin Desarrollar'),
           ('Tercer Milenio', 'Tercer Milenio'),('Asentamiento Carbonell', 'Asentamiento Carbonell'),
           ('Ciudadela Confamiliar', 'Ciudadela Confamiliar'),('Carlos Pizarro', 'Carlos Pizarro'),
           ('Acropolis', 'Acropolis'),('Camilo Torres', 'Camilo Torres'),('Santa Inés', 'Santa Inés'),
           ('El Triangulo', 'El Triangulo'),('Villa del Rio', 'Villa del Rio'),('Los Andaquies', 'Los Andaquies'),
           ('Rodrigo Lara Bonilla', 'Rodrigo Lara Bonilla'),('Candido Leguizamo', 'Candido Leguizamo'),
           ('La Inmaculada', 'La Inmaculada'),('Colmenar', 'Colmenar'),('La Riviera', 'La Riviera'),
           ('Villa Magdalena', 'Villa Magdalena'),('Las Mercedes', 'Las Mercedes'),('Mira Rio', 'Mira Rio'),
           ('Chicala', 'Chicala'),('Mansiones del Norte', 'Mansiones del Norte'),('El Cortijo', 'El Cortijo'),
           ('Villa Carolina', 'Villa Carolina'),('Villa Cecilia', 'Villa Cecilia'),('Las Granjas', 'Las Granjas'),
           ('Aeropuerto Benito Salas', 'Aeropuerto Benito Salas'),('Aeropuerto', 'Aeropuerto'),
           ('Álamos Norte', 'Álamos Norte'),('Camino Real', 'Camino Real'),('Los Cámbulos', 'Los Cámbulos'),
           ('Gualanday', 'Gualanday'),('El Rosal', 'El Rosal'),('Los Pinos', 'Los Pinos'),
           ('Villa Nubia', 'Villa Nubia'),('Asentamiento del Magdalena', 'Asentamiento del Magdalena'),
           ('El Lago', 'El Lago'),('Caracoli', 'Caracoli'),('Sevilla', 'Sevilla'),
           ('José Eustacio Rivera', 'José Eustacio Rivera'),('Tenerife', 'Tenerife'),('Las Delicias', 'Las Delicias'),
           ('Campo Nuñez', 'Campo Nuñez'),('Rojas Trujillo', 'Rojas Trujillo'),('Chapinero', 'Chapinero'),
           ('Quirinal', 'Quirinal'),('La Toma', 'La Toma'),('Batallón', 'Batallón'),('El Jardín', 'El Jardín'),
           ('Los Guaduales', 'Los Guaduales'),('Villa Rosa', 'Villa Rosa'),('La Colina', 'La Colina'),
           ('La Libertad', 'La Libertad'),('Los Buganviles', 'Los Buganviles'),('El Vergel', 'El Vergel'),
           ('Primero de Mayo', 'Primero de Mayo'),('Monserrate', 'Monserrate'),('Villa Café', 'Villa Café'),
           ('El Tesoro', 'El Tesoro'),('Sector El Condor', 'Sector El Condor'),
           ('La Amistad-Oro Negro', 'La Amistad-Oro Negro'),('Antonio Nariño', 'Antonio Nariño'),
           ('Enrique Olaya Herrera', 'Enrique Olaya Herrera'),('Pablo VI', 'Pablo VI'),('Los Colores', 'Los Colores'),
           ('La Rioja', 'La Rioja'),('Misael Pastrana Borrero', 'Misael Pastrana Borrero'),('Salitre', 'Salitre'),
           ('Sector Barreiro', 'Sector Barreiro'),('El Triunfo', 'El Triunfo'),
           ('Asentamiento Miraflores', 'Asentamiento Miraflores'),('Las Palmas', 'Las Palmas'),
           ('Victor Félix Díaz', 'Victor Félix Díaz'),('Siglo XXI Oriente', 'Siglo XXI Oriente'),
           ('Asentamiento Palmas II', 'Asentamiento Palmas II'),('Asentamiento Neiva Yá', 'Asentamiento Neiva Yá'),
           ('Las Brisas', 'Las Brisas'),('Prado Alto', 'Prado Alto'),('La Gaitana', 'La Gaitana'),
           ('Calixto Leiva', 'Calixto Leiva'),('San Martin de Porres', 'San Martin de Porres'),('Obrero', 'Obrero'),
           ('Ventilador', 'Ventilador'),('Ipanema', 'Ipanema'),('Alfonso López', 'Alfonso López'),
           ('Las Américas', 'Las Américas'),('Los Parques', 'Los Parques'),('Las Acacias', 'Las Acacias'),
           ('La Florida', 'La Florida'),('San Carlos', 'San Carlos'),('Panorama', 'Panorama'),
           ('Rafael Azuero Manchola', 'Rafael Azuero Manchola'),
           ('Asentamiento Sector Santa Isabel', 'Asentamiento Sector Santa Isabel'),
           ('Asentamiento Sector Bogota', 'Asentamiento Sector Bogota'),
           ('Asentamiento Sector Galan', 'Asentamiento Sector Galan'),('Santa Isabel', 'Santa Isabel'),
           ('Bogotá', 'Bogotá'),('José Antonio Galan', 'José Antonio Galan'),('Pozo Azul', 'Pozo Azul'),
           ('Arismendi Mora Perdomo', 'Arismendi Mora Perdomo'),('Loma Linda', 'Loma Linda'),('Timanco', 'Timanco'),
           ('Andalucia', 'Andalucia'),('Bellavista', 'Bellavista'),('Canaima', 'Canaima'),('Manzanares', 'Manzanares'),
           ('Puertas del Sol', 'Puertas del Sol'),('Sector Trapichito', 'Sector Trapichito'),('Limonar', 'Limonar'),
           ('El Oasis', 'El Oasis'),('San Jorge', 'San Jorge'),('Los Potros', 'Los Potros'),
           ('Los Martires', 'Los Martires'),('El Centro', 'El Centro'),('Altico', 'Altico'),
           ('El Estadio', 'El Estadio'),('Diego de Ospina', 'Diego de Ospina'),('San Pedro', 'San Pedro'),
           ('San José', 'San José')]

comunas =[
    ('Comuna 1','Comuna 1'),('Comuna 2','Comuna 2'),('Comuna 3','Comuna 3'),('Comuna 4','Comuna 4'),
    ('Comuna 5','Comuna 5'),('Comuna 6','Comuna 6'),('Comuna 7','Comuna 7'),('Comuna 8','Comuna 8'),
    ('Comuna 9','Comuna 9'),('Comuna 10','Comuna 10')
]

sitiosDeInteres =[
    ('centro de Convenciones José Eustásio Rivera','centro de Convenciones José Eustásio Rivera'),
    ('Monumentos a los Potros','Monumentos a los Potros'),('Centro Comercial San Pedro Plaza','Centro Comercial San Pedro Plaza'),
    ('Parque de la Musica','Parque de la Musica'),('Parque Leesburg','Parque Leesburg'),
    ('La Cruz Roja','La Cruz Roja'),('Los Comuneros','Los Comuneros')
]

class Rol(models.Model):
    rolNombre = models.CharField(max_length=50)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rolNombre}"

class Usuario(models.Model):
    usuNombre = models.CharField(unique=True,max_length=21)
    usuCorreo = models.CharField(unique=True,max_length=50)
    usuPassword = models.CharField(max_length=128)  # Almacenar la contraseña en un campo de longitud suficiente
    usuCreadoConGoogle = models.BooleanField(default=False)
    usuTokenCambioContrasena = models.CharField(max_length=50, null=True, blank=True)
    usuRol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def set_password(self, password):
        # Utilizar SHA-256 para encriptar la contraseña
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        self.usuPassword = sha256.hexdigest()

    def check_password(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        hashed_password = sha256.hexdigest()
        return hashed_password == self.usuPassword

    def __str__(self):
        return f"{self.usuNombre}"

class Ruta(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activa'),
        ('I', 'Inactiva'),
    ]
    rutNumero = models.IntegerField(db_comment="Numero de la ruta del bus", null=True)
    rutPrecio = models.TextField(db_comment="Precio de la Ruta",null=True)
    rutEmpresa = models.TextField(db_comment="Id de Empresa")
    rutEstado = models.CharField(
        db_comment="Activa y desactiva la ruta",
        max_length=1,
        choices=ESTADO_CHOICES,
        default='A',
    )
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def __str__(self):
        return f"{self.rutNumero}"
    
class Comentario(models.Model):
    comDescripcion = models.CharField(max_length=100)
    comValoracion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],null=True
    )  # Valor de valoración entre 1 y 5
    comUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True)
    comRuta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraActualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comDescripcion} - Valoración: {self.comValoracion}"
    
class DetalleRuta(models.Model):
    detRuta = models.ForeignKey(Ruta,on_delete=models.PROTECT,
                                    db_comment="Hace referencia a la ruta que se va a registrar")
    detLatitud = models.TextField(db_comment="Latitud de la trayectoria de la ruta")
    detLongitud = models.TextField(db_comment="Longitud de la trayectoria de la ruta")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def __str__(self)->str:
        return f"{self.detLatitud}->{self.detLongitud}"

class UbicacionRuta(models.Model):
    ubiRuta = models.ForeignKey(Ruta,on_delete=models.PROTECT,
                                    db_comment="Hace referencia a la ruta que se va a registrar")
    ubiBarrio = models.TextField(db_comment="Barrio por donde pasa la ruta")
    ubiComuna = models.TextField(db_comment="Comuna por donde pasa la ruta")
    ubiSitioDeInteres = models.TextField(db_comment="Sitio de interes por donde pasa la ruta")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def __str__(self)->str:
        return f"{self.ubiBarrio}->{self.ubiComuna}->{self.ubiSitioDeInteres}"

class FavoritoRuta(models.Model):
    favRuta = models.ForeignKey(Ruta,on_delete=models.PROTECT,
                                    db_comment="Hace referencia a la ruta que se va a añadir a favorito")
    favUsuario = models.ForeignKey(Usuario,on_delete=models.PROTECT, null=True,db_comment="Hace referencia al Usuario que añade a favorito")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

    def __str__(self)->str:
        return f"{self.ubiBarrio}->{self.ubiComuna}->{self.ubiSitioDeInteres}"