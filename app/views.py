import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from app import forms, models
from app.fixtures import generate_services
from app.utils import check_administrator
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.error.transbank_error import TransbankError

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
    context = {
        'service': service,
    }
    return render(request, 'create-reservation.html', context)

def create_reservation_and_payment(request, service_id):
    print('create_reservation_and_payment called')
    if request.method == 'POST':
        data = json.loads(request.body)
        service = get_object_or_404(models.Service, id=service_id)
        duration = data.get('duration', 1)
        total = service.price * duration
        service = get_object_or_404(models.Service, id=service_id)
        post_data = {
            'date': data.get('date'),
            'time': data.get('time'),
            'duration': duration,
            'service': service_id,
            'client': request.user.id,
            'total': total
        }
        form = forms.ReservationForm(post_data)
        if form.is_valid():
            reservation = form.save()
            buy_order = 'buy_order_' + str(reservation.id)
            session_id = 'session_id_' + str(reservation.id)
            return_url = request.build_absolute_uri(reverse('payment_success', args=[reservation.id]))
            options = WebpayOptions(
                commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
                api_key=IntegrationApiKeys.WEBPAY,
                integration_type=IntegrationType.TEST
            )

            transaction = Transaction(options)

            try:
                response = transaction.create(buy_order, session_id, total, return_url)
                print("Transaction created successfully:", response)
                return JsonResponse({
                    'url_webpay': response['url'] + "?token_ws=" + response['token'],
                    'token': response['token']
                })
            except TransbankError as e:
                print("Error during transaction creation:", e.message)
                return JsonResponse({"error": e.message}, status=500)

        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors,
                'message': 'Failed to create reservation.'
            }, status=400)

def payment_success(request, reservation_id):
    reservation = get_object_or_404(models.Reservation, id=reservation_id)
    print('reservation:')
    print(reservation)
    token_ws = request.GET.get('token_ws')
    reservation.payed = True
    reservation.save()
    context = {
        'reservation': reservation,
        'token_ws': token_ws
    }
    return render(request, 'payment-success.html', context)

def get_reservations(request):
    reservations = models.Reservation.objects.all()
    reservations_data = []
    for reservation in reservations:
        reservations_data.append({
            'id': reservation.id,
            'date': reservation.date.strftime('%Y-%m-%d'),
            'time': reservation.time.strftime('%H:%M:%S'),
            'duration': reservation.duration,
            'service': reservation.service.title,
            'client': reservation.client.email,
            'total': reservation.total,
            'payed': reservation.payed
        })
    return JsonResponse(reservations_data, safe=False)

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


