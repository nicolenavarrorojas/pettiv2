from django.test import TestCase, Client, override_settings
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
from app.models import Service, Reservation
from app.forms import SignupForm
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, time

@override_settings(TESTING=True)
class UserModelTest(TestCase):
    """Prueba para el modelo User personalizado"""
    
    def test_create_partner_user(self):
        """Prueba la creación de usuario partner con campos específicos"""
        UserModel = get_user_model()
        partner = UserModel.objects.create_user(
            email='partner@example.com',
            password='testpassword',
            is_partner=True,
            description='Expert pet groomer',
            phone_number='1234567890',
            address='123 Pet Street'
        )
        
        self.assertTrue(partner.is_partner)
        self.assertEqual(partner.email, 'partner@example.com')
        self.assertEqual(partner.description, 'Expert pet groomer')
        self.assertEqual(partner.phone_number, '1234567890')
        self.assertTrue(partner.check_password('testpassword'))


@override_settings(TESTING=True)
class ReservationModelTest(TestCase):
    """Prueba para el modelo Reservation"""
    
    def setUp(self):
        UserModel = get_user_model()
        self.partner = UserModel.objects.create_user(
            email='partner@example.com',
            password='testpassword',
            is_partner=True
        )
        self.client_user = UserModel.objects.create_user(
            email='client@example.com',
            password='testpassword'
        )
        
        dummy_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        self.service = Service.objects.create(
            service_type=Service.GROOMING,
            title='Pet Grooming',
            description='Professional grooming',
            price=15000,
            partner=self.partner,
            image=dummy_image
        )
    
    def test_reservation_creation_and_relationships(self):
        """Prueba creación de reserva y sus relaciones con servicio y cliente"""
        reservation = Reservation.objects.create(
            date=date(2024, 12, 25),
            time=time(14, 30),
            duration=2,
            service=self.service,
            client=self.client_user
        )
        
        # Verificar creación
        self.assertEqual(reservation.date, date(2024, 12, 25))
        self.assertEqual(reservation.duration, 2)
        self.assertEqual(reservation.service, self.service)
        self.assertEqual(reservation.client, self.client_user)
        
        # Verificar relaciones
        self.assertEqual(self.service.reservations.count(), 1)
        self.assertEqual(self.client_user.reservations.count(), 1)
        
        # Verificar string representation
        expected_str = f'Reservation for Pet Grooming on 2024-12-25 at 14:30:00 by client@example.com'
        self.assertEqual(str(reservation), expected_str)


@override_settings(TESTING=True)
class SignupFormTest(TestCase):
    """Prueba para el formulario de registro"""
    
    def test_signup_form_validation(self):
        """Prueba validación del formulario de registro - caso válido e inválido"""
        # Caso válido
        valid_data = {
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = SignupForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
        # Caso inválido - contraseñas no coinciden
        invalid_data = {
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        form = SignupForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


@override_settings(TESTING=True)  
class ServicesViewTest(TestCase):
    
    def setUp(self):
        # Crear usuarios de prueba
        UserModel = get_user_model()
        self.partner1 = UserModel.objects.create_user(
            username='partner1',
            email='partner1@gmail.com',
            password='testpassword',
            is_partner=True
        )
        self.partner2 = UserModel.objects.create_user(
            username='partner2',
            email='partner2@gmail.com',
            password='testpassword',
            is_partner=True
        )
        
        # Crear imagen dummy para los tests
        dummy_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        # Crear servicios de prueba
        self.grooming_service = Service.objects.create(
            service_type=Service.GROOMING,
            title='Estética Premium Test',
            description='Servicio de prueba para estética',
            price=15000,
            partner=self.partner1,
            image=dummy_image
        )
        
        self.walking_service = Service.objects.create(
            service_type=Service.WALKING,
            title='Paseo Test',
            description='Servicio de prueba para paseo',
            price=10000,
            partner=self.partner1,
            image=dummy_image
        )
        
        self.sitting_service = Service.objects.create(
            service_type=Service.SITTING,
            title='Cuidado Test',
            description='Servicio de prueba para cuidado',
            price=20000,
            partner=self.partner2,
            image=dummy_image
        )
        
        self.client = Client()
    
    @patch('app.views.generate_services')
    def test_services_view_all(self, mock_generate):
        # Mock para evitar que se ejecute generate_services
        mock_generate.return_value = None
        
        response = self.client.get(reverse('services'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')
        
        services_in_context = response.context['services']
        self.assertEqual(services_in_context.count(), 3)
        
        self.assertIsNone(response.context['service_type'])
    
    @patch('app.views.generate_services')
    def test_services_view_filtered_grooming(self, mock_generate):
        mock_generate.return_value = None
        
        response = self.client.get(f"{reverse('services')}?service_type=grooming")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'grooming')
        
        self.assertEqual(response.context['service_type'], 'grooming')
    
    @patch('app.views.generate_services')
    def test_services_view_filtered_walking(self, mock_generate):
        mock_generate.return_value = None
        
        response = self.client.get(f"{reverse('services')}?service_type=walking")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'walking')
        
        self.assertEqual(response.context['service_type'], 'walking')
    
    @patch('app.views.generate_services')
    def test_services_view_filtered_sitting(self, mock_generate):
        mock_generate.return_value = None
        
        response = self.client.get(f"{reverse('services')}?service_type=sitting")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'sitting')
        
        self.assertEqual(response.context['service_type'], 'sitting')
    
    @patch('app.views.generate_services')
    def test_services_view_invalid_filter(self, mock_generate):
        mock_generate.return_value = None
        
        response = self.client.get(f"{reverse('services')}?service_type=invalid")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 3)
        
        self.assertEqual(response.context['service_type'], 'invalid')