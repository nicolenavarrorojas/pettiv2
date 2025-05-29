from app import models
import sys


def generate_partners():


    partners = [
        {'email': 'partner1@gmail.com', 'first_name': 'Camilo', 'last_name': 'Gonzalez'}, 
        {'email':'partner2@gmail.com','first_name': 'Fernanda', 'last_name': 'Castillo'}
    ]

    for partner in partners:
        if not models.User.objects.filter(email=partner['email']).exists():
            models.User.objects.create_user(
                email=partner['email'],
                first_name=partner['first_name'],
                last_name=partner['last_name'],
                is_administrator= False,
                is_partner= True,
                description= 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                phone_number = '1234567890',
                address = '123 Main St, City, Country',
                password = '3265plok',
            )
    

def generate_services():
    if 'tests' in sys.argv:
        return
    
    generate_partners()
    services = [ 
        {
            'service_type': models.Service.GROOMING, 
            'title': 'Estética Premium para Mascotas', 
            'description':'Servicio profesional que incluye baño, corte de pelo, corte de uñas y limpieza de oídos.',
            'price': 18000,
            'partner': models.User.objects.get(email='partner1@gmail.com'),
            'image': 'service_images/esteticaperros.jpg'
        },
        {
            'service_type': models.Service.GROOMING, 
            'title': 'Estética Básica', 
            'description':'Servicio básico de estética que incluye baño y cepillado.',
            'price': 12000,
            'partner': models.User.objects.get(email='partner1@gmail.com'),
            'image': 'service_images/esteticabasica.jpg'
        },
        {
            'service_type': models.Service.WALKING, 
            'title': 'Paseo Diario para Perros', 
            'description':'Paseos regulares para que tu perro se mantenga sano y feliz mientras estás ocupado.',
            'price': 10000,
            'partner': models.User.objects.get(email='partner1@gmail.com'),
            'image': 'service_images/paseomascotas2.jpg'
        },
        {
            'service_type': models.Service.WALKING, 
            'title': 'Paseo de Fin de Semana', 
            'description':'Paseos de fin de semana para tu perro mientras tú te diviertes.',
            'price': 8000,
            'partner': models.User.objects.get(email='partner2@gmail.com'),
            'image': 'service_images/paseomascotas3.jpg'
        },
        {
            'service_type': models.Service.SITTING, 
            'title': 'Cuidado Nocturno de Mascotas', 
            'description':'Cuidado amoroso para tus mascotas en casa mientras estás fuera. Incluye alimentación, juegos y compañía.',
            'price': 28000,
            'partner': models.User.objects.get(email='partner2@gmail.com'),
            'image': 'service_images/cuidadonocturno.jpg'
        },
        {
            'service_type': models.Service.SITTING, 
            'title': 'Cuidado durante Vacaciones', 
            'description':'Cuidado extendido para tus mascotas mientras estás de vacaciones. Visitas diarias, alimentación y atención.',
            'price': 35000,
            'partner': models.User.objects.get(email='partner2@gmail.com'),
            'image': 'service_images/paseomascotas.jpg'
        },
    ]
    for service in services:
        if not models.Service.objects.filter(title=service['title']).exists():
            models.Service.objects.create(
                service_type=service['service_type'], 
                title=service['title'], 
                description=service['description'],
                price=service['price'],
                partner=service['partner'],
                image=service['image']
            )
