from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def services(request):
    return render(request, 'services.html')

def admin_dashboard(request):
    return render(request, 'admin-dashboard.html')

def admin_view(request):
    return render(request, 'admin.html')

def payment(request):
    return render(request, 'payment.html')
