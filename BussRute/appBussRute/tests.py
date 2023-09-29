from django.test import TestCase, Client, override_settings
from appBussRute.models import *
from appBussRute.views import *
from django.http import HttpResponse
import hashlib
from django.urls import reverse
from django.core import mail
import re
from bs4 import BeautifulSoup
import pdb
import json

# BLOQUE DE MAURICIO CATAÑO TESTS -------------------------------------------------------------------------------------------

class TestInicioSesion(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.usuario = Usuario.objects.create(
            usuNombre='Mauricio Catano',
            usuCorreo='mp990975@gmail.com',
        )
        self.usuario.set_password('0000')
        self.usuario.save()

    def test_iniciarSesion(self):
        sha256 = hashlib.sha256()
        sha256.update('0000'.encode('utf-8'))
        hashed_password = sha256.hexdigest()

        response = self.client.post(reverse('iniciarSesion'), {
            'correoUsuarioInicioONombreUsuario': 'Mauricio Catano',
            'passwordUsuarioInicio': hashed_password
        })        
        self.assertIsInstance(response, HttpResponse)

        self.assertEqual(response.status_code, 200)  

class TestRegistrarUsuarioConGoogleTestCase(TestCase):
    def setUp(self):
       self.rol = Rol.objects.create(rolNombre="Usuario", id=2)

    def test_registrar_usuario_exitoso(self):
        datos_post = {
            "nombreUsuarioGoogle": "Mauricio",
            "correoUsuarioGoogle": "mp770765@gmail.com",
            "rolId": self.rol.id, 
            "usuCreadoConGoogle": True
        }
        
        response = self.client.post(reverse('enviarNombreUsuario'), datos_post)

        self.assertRedirects(response, '/inicio/')
        
        self.assertTrue(Usuario.objects.filter(usuNombre='Mauricio').exists())

class TestRegistrarUsuario(TestCase):
    def setUp(self):
        self.rol = Rol.objects.create(rolNombre="Usuario", id=2)

    def tearDown(self):
        mail.outbox = []

    def test_registro_y_correo_de_verificacion(self):
        client = Client()
        response = client.post('/registrarCuenta/', {
            'nombreUsuario': 'Santiago',
            'correoUsuario': 'mp770765@gmail.com',
            'passwordUsuario': '0000',
        })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, 'Verificacion del Correo Electronico')

        body = mail.outbox[0].body

        match = re.search(r'letter-spacing:10px">\s*(\w+)\s*</h2>', body)

        if match:
            codigo_de_verificacion = match.group(1)
            
            # Almacena el código de verificación en la sesión
            session = client.session
            session['codigo_verificacion'] = codigo_de_verificacion
            session.save()

            response = client.post('/enviarVerificacionCorreo/', {
                'codigoVerifi': codigo_de_verificacion,
            })

            self.assertEqual(response.status_code, 200)

            try:
                user = Usuario.objects.get(usuNombre='Santiago', usuCorreo='mp770765@gmail.com', usuRol=self.rol)
                print('La cuenta ha sido creada correctamente y tiene el rol correcto.')
            except Usuario.DoesNotExist:
                print('La cuenta no ha sido creada o no tiene el rol correcto.')
                
        else:
            print('No se encontró el código de verificación.')

class TestEnviarCorreoRecuperacion(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(usuNombre="Michell", usuCorreo="2004kevinruiz@gmail.com")

    def tearDown(self):
        mail.outbox = []

    def test_enviar_cambio_contrasena_con_usuario_valido(self):
        response = self.client.post('/enviarCambioContrasena/', {'recuCorreo': '2004kevinruiz@gmail.com'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)

        correo = mail.outbox[0]
        self.assertEqual(correo.subject, 'Solicitud para restablecer contraseña de BussRute')

        soup = BeautifulSoup(correo.body, 'html.parser')

        enlace = soup.find('a')

        url = enlace['href']
        #print('URL del enlace:', url)

        # Extrae el token de la URL
        token = url.split('=')[1]

        self.usuario.usuTokenCambioContrasena = token
        self.usuario.save()

        self.assertEqual(self.client.session['token'], token)

        response_cambio_contrasena = self.client.get(url)

        self.assertEqual(response_cambio_contrasena.status_code, 200)

        self.assertTemplateUsed(response_cambio_contrasena, 'cambiarContrasena.html')

        self.assertEqual(self.client.session['token'], token)

        nueva_contraseña = '0004'
        response_cambio_contrasena_post = self.client.post('/cambioContrasena/', {'pasNuevaContraseña': nueva_contraseña})

        self.assertEqual(response_cambio_contrasena_post.status_code, 200)

        self.assertTemplateUsed(response_cambio_contrasena_post, 'cambiarContrasena.html')

        self.assertContains(response_cambio_contrasena_post, 'Contraseña cambiada con éxito')

        print('Contraseña cambiada correctamente')

class DesactivarOActivarViewTest(TestCase):
    def setUp(self):
        # Crea una instancia de Ruta para usar en las pruebas con estado 'I'
        self.ruta = Ruta.objects.create(rutNumero=23, rutPrecio=3500, rutEmpresa="Coomotor", rutEstado='A', id=2)

    def test_desactivar_o_activar_ruta(self):
        # Obtiene la URL para la vista desactivarOActivar
        url = reverse('desactivarOActivar')

        # Realiza una solicitud POST a la vista
        response = self.client.post(url, {'id': self.ruta.id})

        # Verifica que la respuesta sea un JSON con el mensaje esperado
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'mensaje': 'Estado de la ruta actualizado'}
        )

        # Recarga la instancia de la Ruta desde la base de datos
        self.ruta.refresh_from_db()

        # Verifica que el estado de la ruta haya cambiado de 'I' a 'A'
        self.assertEqual(self.ruta.rutEstado, 'I')
        
        print("El estado de la ruta ha sido actualizado")
        

    def tearDown(self):
        # Limpia cualquier recurso o datos creados durante las pruebas
        self.ruta.delete()

# BLOQUE DE JUAN ORITZ TESTS ------------------------------------------------------------------------------------------------

class EliminarComentarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='testuser', usuCorreo='testuser@test.com', usuPassword='testpassword')
        self.ruta = Ruta.objects.create(rutNumero=1, rutPrecio='5000', rutEmpresa='Empresa Test')
        self.comentario = Comentario.objects.create(comDescripcion='Comentario Test', comValoracion=5, comUsuario=self.usuario, comRuta=self.ruta)

    def test_eliminar_comentario(self):
        response = self.client.get(reverse('eliminarComentario', args=[self.comentario.id]))
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección fue exitosa
        with self.assertRaises(Comentario.DoesNotExist):
            Comentario.objects.get(id=self.comentario.id)  # Verificar que el comentario fue eliminado 
            
class ActualizarComentarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='testuser', usuCorreo='testuser@test.com', usuPassword='testpassword')
        self.ruta = Ruta.objects.create(rutNumero=1, rutPrecio='5000', rutEmpresa='Empresa Test')
        self.comentario = Comentario.objects.create(comDescripcion='Comentario Test', comValoracion=5, comUsuario=self.usuario, comRuta=self.ruta)

    def test_actualizar_comentario(self):
        response = self.client.post(reverse('actualizarComentario', args=[self.comentario.id]), {'txtComentario': 'Comentario Actualizado', 'txtValoracion': 4})
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección fue exitosa
        comentario_actualizado = Comentario.objects.get(id=self.comentario.id)
        self.assertEqual(comentario_actualizado.comDescripcion, 'Comentario Actualizado')  # Verificar que el comentario fue actualizado correctamente
        self.assertEqual(comentario_actualizado.comValoracion, 4)  # Verificar que la valoración fue actualizada correctamente
         
class ConsultarComentarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='testuser', usuCorreo='testuser@test.com', usuPassword='testpassword')
        self.ruta = Ruta.objects.create(rutNumero=1, rutPrecio='5000', rutEmpresa='Empresa Test')
        self.comentario = Comentario.objects.create(comDescripcion='Comentario Test', comValoracion=5, comUsuario=self.usuario, comRuta=self.ruta)

    def test_consultar_comentario(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id  # Simular un usuario en sesión
        session.save()
        
        response = self.client.get(reverse('consultarComentario', args=[self.comentario.id]))
        self.assertEqual(response.status_code, 200)  # Verificar que la respuesta fue exitosa
        self.assertContains(response, 'Comentario Test')  # Verificar que el comentario está en la respuesta 

class AgregarComentarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='testuser', usuCorreo='testuser@test.com', usuPassword='testpassword')
        self.ruta = Ruta.objects.create(rutNumero=1, rutPrecio='5000', rutEmpresa='Empresa Test')

    def test_agregar_comentario(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id  # Simular un usuario en sesión
        session.save()
        
        response = self.client.post(reverse('agregarComentario'), {'txtNombre': 'testuser', 'txtComentario': 'Comentario Test', 'txtValoracion': 5, 'txtRuta': self.ruta.rutNumero})
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección fue exitosa
        comentario = Comentario.objects.get(comDescripcion='Comentario Test')  # Obtener el comentario recién creado
        self.assertIsNotNone(comentario)  # Verificar que el comentario fue creado correctamente

class CerrarSesionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='testuser', usuCorreo='testuser@test.com', usuPassword='testpassword')

    def test_cerrar_sesion(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id  # Simular un usuario en sesión
        session.save()
        
        response = self.client.get(reverse('cerrarSesion'))
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección fue exitosa
        self.assertNotIn('usuario_id', self.client.session)  # Verificar que 'usuario_id' ya no está en la sesión

# BLOQUE DE SANTIAGO VARGAS TESTS ------------------------------------------------------------------------------------------------

class VisualizarRutasTestCase(TestCase):
    def setUp(self):
        self.ruta = Ruta.objects.create(
            rutNumero=8,
            rutPrecio='2400',
            rutEmpresa='Coomotor',
            rutEstado='A'
        )

    def test_visualizar_rutas(self):
        # Realiza una solicitud GET a la vista
        response = self.client.get("/visualizarRutas/")  # Reemplaza 'nombre_de_la_vista' con la URL de la vista

        # Verifica que la vista responda con un código 200 (éxito)
        self.assertEqual(response.status_code, 200)

         # Consulta la lista de rutas desde la base de datos
        rutas_db = Ruta.objects.all()

        # Verifica que la longitud de la lista de rutas en el contexto sea igual a la de la base de datos
        self.assertEqual(len(response.context['rutas']), len(rutas_db))

        # Compara los campos de las rutas en el contexto con las de la base de datos
        for i, ruta_context in enumerate(response.context['rutas']):
            self.assertEqual(ruta_context.rutNumero, rutas_db[i].rutNumero)
            self.assertEqual(ruta_context.rutPrecio, rutas_db[i].rutPrecio)
            self.assertEqual(ruta_context.rutEmpresa, rutas_db[i].rutEmpresa)
            self.assertEqual(ruta_context.rutEstado, rutas_db[i].rutEstado)

class EliminarFavoritoViewTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
        usuNombre="usuario_de_prueba",             
        usuCorreo="usuario@example.com",
        usuPassword="contra_de_prueba",
        usuRol=Rol.objects.create(rolNombre='Usuario'))
        self.ruta = Ruta.objects.create(rutNumero=8, rutPrecio='2400', rutEmpresa='Coomotor')
        self.favorito = FavoritoRuta.objects.create(favRuta=self.ruta,favUsuario=self.usuario)
        self.url ="/eliminarFavorito/"  # Asegúrate de ajustar el nombre de la URL según tu configuración

    def test_eliminar_favorito_exitoso(self):
        data = {'numeroRuta': self.ruta.rutNumero}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['mensaje'], "Ruta Favorita Eliminada")
        response_data = response.json()
        self.mensaje = response_data.get('mensaje', '')
    def tearDown(self):
        # Imprime el mensaje
        print(self.mensaje)
                  
class TestRegistroFavorito(TestCase):
    def setUp(self):
        #Crea un usuario de prueba
        self.client = Client()
        self.usuario = Usuario.objects.create(usuNombre='usuario_de_prueba', usuCorreo='usuario@example.com', usuPassword='contra_de_prueba')
        self.ruta = Ruta.objects.create(rutNumero=8, rutPrecio='2400', rutEmpresa='Coomotor')

    def test_registro_favorito(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id  # Simular un usuario en sesión
        session.save()
        # Define los datos que enviarás en la solicitud POST
        data = {
            'ruta': self.ruta.rutNumero,
        }

        url = '/registroFavorito/'  # Ajusta la URL a tu vista
        response = self.client.post(url, data)

        # Verifica que la respuesta sea exitosa (código de respuesta HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Analiza el contenido de la respuesta JSON
        response_data = response.json()
        self.assertEqual(FavoritoRuta.objects.count(), 1)

        # Verifica que el mensaje sea el esperado
        self.assertEqual(response_data['mensaje'], "Ruta Añadida a Favorito Correctamente")
        self.mensaje = response_data.get('mensaje', '')
    def tearDown(self):
        # Imprime el mensaje
        print(self.mensaje)
         
class TestEliminarRuta(TestCase):
    def test_eliminar_ruta_exitoso(self):
        # Crear una instancia de Ruta para eliminar
        ruta = Ruta.objects.create(rutNumero=8, rutPrecio='2400', rutEmpresa='Coomotor')
        detalle = DetalleRuta.objects.create(detRuta=ruta, detLatitud=2.941819435241974, detLongitud=-75.28997301713491)
        ubicacion = UbicacionRuta.objects.create(ubiRuta=ruta, ubiBarrio='Altico', ubiComuna='Comuna 4', ubiSitioDeInteres='Hospital')

        # Define los datos que enviarás en la solicitud POST
        data = {
            'id': ruta.id,
        }

        url = '/eliminarRuta/'  # Esta es la URL real de tu vista
        response = self.client.post(url, data)

        # Verifica que la respuesta sea exitosa (código de respuesta HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Analiza el contenido de la respuesta JSON
        response_data = json.loads(response.content.decode('utf-8'))

        # Verifica que el mensaje sea el esperado
        self.assertEqual(response_data['mensaje'], "Ruta Eliminada")

        # Verifica que la ruta, detalle y ubicación se hayan eliminado correctamente
        self.assertEqual(Ruta.objects.filter(id=ruta.id).count(), 0)
        self.assertEqual(DetalleRuta.objects.filter(detRuta=ruta).count(), 0)
        self.assertEqual(UbicacionRuta.objects.filter(ubiRuta=ruta).count(), 0)
        # Analiza el contenido de la respuesta JSON
        response_data = json.loads(response.content.decode('utf-8'))

        # Verifica que el mensaje sea el esperado
        self.assertEqual(response_data['mensaje'], "Ruta Eliminada")

        self.mensaje = response_data.get('mensaje', '')

    def tearDown(self):
        # Imprime el mensaje
        print(self.mensaje)
         
class TestRegistroRuta(TestCase):
    def test_registro_ruta_exitoso(self):
        # Define los datos que enviarás en la solicitud POST
        data = {
            'numeroRuta': 8,
            'precio': '2400',
            'empresa': 'Coomotor',
            'detalle': json.dumps([
                {'latitud': 2.941819435241974, 'longitud': -75.28997301713491},
                {'latitud': 2.925534316101293, 'longitud': -75.2863676122053},
                {'latitud': 2.9373159049785045, 'longitud': -75.26736857052656},
            ]),
            'ubicacion': json.dumps([{'barrio': 'Altico', 'comuna': 'Comuna 4', 'sitioDeInteres': 'Hospital'}])
            }

        url = '/registroRuta/'  # Esta es la URL real de tu vista
        response = self.client.post(url, data)

        # Verifica que la respuesta sea exitosa (código de respuesta HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que se haya registrado la ruta correctamente en la base de datos
        self.assertEqual(Ruta.objects.count(), 1)
        self.assertEqual(DetalleRuta.objects.count(), 3)
        self.assertEqual(UbicacionRuta.objects.count(), 1)
        # Puedes agregar más aserciones para verificar otros aspectos de la respuesta si es necesario
        # Analiza el contenido de la respuesta JSON
        response_data = json.loads(response.content.decode('utf-8'))

        # Verifica que el mensaje sea el esperado
        self.assertEqual(response_data['mensaje'], "Se ha registrado la Ruta Correctamente")

        self.mensaje = response_data.get('mensaje', '')

    def tearDown(self):
        # Imprime el mensaje
        print(self.mensaje)
