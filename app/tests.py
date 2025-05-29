from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Service
from django.core.files.uploadedfile import SimpleUploadedFile

class ServicesViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.partner1 = User.objects.create_user(
            username='partner1',
            email='partner1@gmail.com',
            password='testpassword',
            is_partner=True
        )
        cls.partner2 = User.objects.create_user(
            username='partner2',
            email='partner2@gmail.com',
            password='testpassword',
            is_partner=True
        )
        
        dummy_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        cls.grooming_service = Service.objects.create(
            service_type=Service.GROOMING,
            title='Estética Premium Test',
            description='Servicio de prueba para estética',
            price=15000,
            partner=cls.partner1,
            image=dummy_image
        )
        
        cls.walking_service = Service.objects.create(
            service_type=Service.WALKING,
            title='Paseo Test',
            description='Servicio de prueba para paseo',
            price=10000,
            partner=cls.partner1,
            image=dummy_image
        )
        
        cls.sitting_service = Service.objects.create(
            service_type=Service.SITTING,
            title='Cuidado Test',
            description='Servicio de prueba para cuidado',
            price=20000,
            partner=cls.partner2,
            image=dummy_image
        )
    
    def setUp(self):
        self.client = Client()
        
    def test_services_view_all(self):
        response = self.client.get(reverse('services'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')
        
        services_in_context = response.context['services']
        self.assertEqual(services_in_context.count(), 3)
        
        self.assertIsNone(response.context['service_type'])
    
    def test_services_view_filtered_grooming(self):
        response = self.client.get(f"{reverse('services')}?service_type=grooming")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'grooming')
        
        self.assertEqual(response.context['service_type'], 'grooming')
    
    def test_services_view_filtered_walking(self):
        response = self.client.get(f"{reverse('services')}?service_type=walking")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'walking')
        
        self.assertEqual(response.context['service_type'], 'walking')
    
    def test_services_view_filtered_sitting(self):
        response = self.client.get(f"{reverse('services')}?service_type=sitting")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 1)
        self.assertEqual(services_in_context.first().service_type, 'sitting')
        
        self.assertEqual(response.context['service_type'], 'sitting')
    
    def test_services_view_invalid_filter(self):
        response = self.client.get(f"{reverse('services')}?service_type=invalid")
        
        self.assertEqual(response.status_code, 200)
        services_in_context = response.context['services']
        
        self.assertEqual(services_in_context.count(), 3)
        
        self.assertEqual(response.context['service_type'], 'invalid')
