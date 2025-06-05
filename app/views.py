from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from app import forms, models
from app.fixtures import generate_services
from app.utils import check_administrator

def index(request):
    generate_services()
    recent_services = models.Service.objects.all().order_by('-upload_date')[:3]
    context = {
        'recent_services': recent_services
    }
    return render(request,'index.html', context)

def login_view(request):
    generate_services()
    return render(request, 'login.html')

def register(request):
    if request.method == 'GET':
        generate_services()
        return render(request, 'register.html')
    elif request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(
                username=email,
                password=raw_password
            )
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
            
        else:
            print('form is invalid')
            print(form.errors)
        context = {
            'form': form
        }
        return render(request, 'register.html', context)
    else:
        raise Exception('Invalid request method')

def services(request):
    generate_services()
    service_type = request.GET.get('service_type', None)
    search = request.GET.get('search', None)
    if service_type in ['grooming', 'walking', 'sitting']:
        services = models.Service.objects.filter(service_type=service_type)
    else:
        services = models.Service.objects.all()
    context = {
        'services': services,
        'service_type': service_type
    }
    return render(request, 'services.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@check_administrator
def admin_dashboard(request):
    return render(request, 'admin-dashboard.html')

def create_reservation(request, service_id):
    service = get_object_or_404(models.Service, id=service_id)

    if request.method == 'POST':
        print('POST request received for create_reservation')
        print(request.POST)
        post_data = request.POST.copy()
        post_data['service'] = service_id
        post_data['client'] = request.user.id 

        form = forms.ReservationForm(post_data)
        if form.is_valid():
            print('Form is valid')
            reservation = form.save()
            print('reservation:')
            print(reservation)
            return HttpResponseRedirect(reverse('payment'))
        else:
            print('Form is invalid')
            print(form.errors)
            context = {
                'service': service,
                'form': form
            }
            return render(request, 'create-reservation.html', context)
        
    context = {
        'service': service,
    }
    return render(request, 'create-reservation.html', context)

def payment(request):
    return render(request, 'payment.html')

def add_service(request):
    return render(request, 'add-service.html')

def client_profile(request):
    return render(request, 'client-profile.html')

def partner_profile_form(request):
    return render(request, 'partner-profile-form.html')

def partner_profile(request):
    return render(request, 'partner-profile.html')

def partner_public_view(request):
    return render(request, 'partner-public-view.html')


