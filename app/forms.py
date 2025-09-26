import datetime
from django import forms
from app.models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ['agent','is_active','created_at','company']

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        exclude = ['agent','client','company','is_active','created_at']



    