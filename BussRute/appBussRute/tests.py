from django.test import TestCase, Client, override_settings
from appBussRute.models import Usuario, Rol, Ruta, FavoritoRuta
from appBussRute.views import registrarseUsuario, enviarCorreo, generarCodigoVerificacion 
from django.http import HttpResponse
import hashlib
from django.urls import reverse
from django.core import mail
import re
from bs4 import BeautifulSoup
import pdb


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

