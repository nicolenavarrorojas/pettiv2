from django import forms
from django.contrib.auth.forms import UserCreationForm
from app import models

class SignupForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]

class ReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = [
            'date',
            'time',
            'duration',
            'service',
            'client'
        ]
