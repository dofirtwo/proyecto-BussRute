from django.test import RequestFactory,TestCase
from .views import *
from .models import *
from django.urls import reverse

 #import unittest
# Create your tests here.

class TestRegistroUsuario(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_registro_usuario_exitoso(self):
        usuario_no_existente = Usuario.objects.filter(usuCorreo="mp990975@gmail.com").first()
        self.assertIsNone(usuario_no_existente)

        request = self.factory.post('registrarCuenta/', {
            'nombreUsuario': 'Mauricio',
            'correoUsuario': 'mp990975@gmail.com',
            'passwordUsuario': '1234'
        })
        print(request)
        # Llama a la función registrarseUsuario
        #response = registrarseUsuario(request)
        request = self.client.get(reverse('crearCuenta.html'))

        self.assertEqual(request.status_code, 200)

        # Verifica que la respuesta sea exitosa (código de respuesta HTTP 200)
        self.assertContains(request, "Correo de verificación enviado.")

        # Verifica que se haya creado una instancia de usuario en la base de datos
        usuario_creado = Usuario.objects.filter(usuCorreo="mp990975@gmail.com").first()
        self.assertIsNotNone(usuario_creado)

        # Verifica que los datos de sesión se hayan configurado correctamente
        self.assertEqual(request.session['nombreUsuario'], 'Mauricio')
        self.assertEqual(request.session['correoUsuario'], 'mp990975@gmail.com')
        self.assertEqual(request.session['contrasena'], '1234')
        self.assertTrue(request.session['registro_completado'])

    def test_registro_usuario_correo_existente(self):
        # Crea una instancia de usuario en la base de datos
        usuario_existente = Usuario.objects.create(usuCorreo="mp990975@gmail.com")

        # Crea una solicitud de prueba con un correo existente
        request = self.factory.post('/registro/', {
            'nombreUsuario': 'Mauricio Cataño',
            'correoUsuario': 'mp990975@gmail.com',
            'passwordUsuario': '123456'
        })

        # Llama a la función registrarseUsuario
        response = registrarseUsuario(request)

        # Verifica que la respuesta redireccione a la página de inicio de sesión
        self.assertEqual(response.status_code, 200)  # Puedes ajustar esto según tu lógica de redirección

        # Verifica que se muestre un mensaje de error apropiado
        mensaje_esperado = "Este correo ya se encuentra registrado."
        self.assertIn(mensaje_esperado, str(response.content))

        # Verifica que no se haya creado una nueva instancia de usuario en la base de datos
        usuario_creado = Usuario.objects.filter(usuCorreo="correo@ejemplo.com").first()
        self.assertIsNotNone(usuario_existente)
        self.assertIsNone(usuario_creado)

    # Puedes agregar más pruebas para otros casos aquí

# if __name__ == '__main__':
#     unittest.main()
