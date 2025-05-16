from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from app import forms
from app.fixtures import generate_services
from app.utils import check_administrator

def index(request):
    generate_services()
    return render(request, 'index.html')

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
    return render(request, 'services.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@check_administrator
def admin_dashboard(request):
    return render(request, 'admin-dashboard.html')

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


