from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Tarea


class TareaCrudTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='usuario1',
            password='claveSegura123',
        )
        self.otro_usuario = User.objects.create_user(
            username='usuario2',
            password='claveSegura123',
        )
        self.tarea = Tarea.objects.create(
            titulo='Estudiar Django',
            descripcion='Practicar el CRUD',
            usuario=self.usuario,
        )

    def test_rutas_protegidas_redirigen_al_login(self):
        respuesta = self.client.get(reverse('tareas'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/iniciarsesion/', respuesta.url)

    def test_usuario_solo_ve_sus_tareas_pendientes(self):
        Tarea.objects.create(
            titulo='Tarea ajena',
            usuario=self.otro_usuario,
        )
        self.client.login(username='usuario1', password='claveSegura123')

        respuesta = self.client.get(reverse('tareas'))

        self.assertContains(respuesta, 'Estudiar Django')
        self.assertNotContains(respuesta, 'Tarea ajena')

    def test_usuario_no_puede_actualizar_tarea_de_otro_usuario(self):
        self.client.login(username='usuario2', password='claveSegura123')

        respuesta = self.client.post(
            reverse('detalle_tarea', args=[self.tarea.id]),
            {'titulo': 'Modificada', 'descripcion': 'No permitida', 'importante': False},
        )

        self.assertEqual(respuesta.status_code, 404)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, 'Estudiar Django')

    def test_completar_y_eliminar_tarea(self):
        self.client.login(username='usuario1', password='claveSegura123')

        completar = self.client.post(
            reverse('tarea_completa', args=[self.tarea.id])
        )
        self.assertRedirects(completar, reverse('tareas'))

        self.tarea.refresh_from_db()
        self.assertIsNotNone(self.tarea.dato_completo)

        eliminar = self.client.post(
            reverse('tarea_eliminar', args=[self.tarea.id])
        )
        self.assertRedirects(eliminar, reverse('tareas'))
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_registro_y_inicio_de_sesion(self):
        respuesta = self.client.post(
            reverse('paginaregistrar'),
            {
                'username': 'nuevo_usuario',
                'password1': 'claveSegura123',
                'password2': 'claveSegura123',
            },
        )
        self.assertRedirects(respuesta, reverse('tareas'))
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

        self.client.logout()
        respuesta = self.client.post(
            reverse('iniciarsesion'),
            {
                'username': 'nuevo_usuario',
                'password': 'claveSegura123',
            },
        )
        self.assertRedirects(respuesta, reverse('tareas'))
