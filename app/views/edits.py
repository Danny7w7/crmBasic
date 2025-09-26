# Standard Python libraries
import datetime

#libreria de paises
from django.shortcuts import render


# Django core libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Application-specific imports
from app.models import *
from ..forms import *
from .decoratorsCompany import *


def clean_field_to_null(value):
    """
    Limpia el valor de un campo. Si el valor está vacío (cadena vacía, None o solo espacios),
    devuelve `None` para que se guarde como NULL en la base de datos.
    """
    if value == '' or value is None or value.strip() == '':
        return None
    return value

def clean_fields_to_null(request, field_names):
    """
    Limpia un conjunto de campos obtenidos desde `request.POST`, 
    convirtiendo los valores vacíos en `None` (NULL en la base de datos).
    Devuelve un diccionario con los campos limpiados.
    """
    cleaned_data = {}
    for field in field_names:
        value = request.POST.get(field)
        cleaned_data[field] = clean_field_to_null(value)
    return cleaned_data

@login_required(login_url='/login') 
def editClient(request, client_id):
    
    client = get_object_or_404(Clients, id=client_id)     

    if request.method == 'POST':

        alert_fields = ['full_name', 'address', 'city', 'country','cod_number','phone_number','email','description' ]

        # Limpiar los campos 
        cleaned_alert_data = clean_fields_to_null(request, alert_fields)

        Alert.objects.filter(id=client_id).update(
            full_name=cleaned_alert_data['full_name'],
            address=cleaned_alert_data['address'],
            city=cleaned_alert_data['city'],
            country=cleaned_alert_data['country'],
            cod_number=cleaned_alert_data['cod_number'],
            phone_number=cleaned_alert_data['phone_number'],
            email=cleaned_alert_data['email'],
            description=cleaned_alert_data['description']
        )
        return redirect('formCreateClients')

    context = {
        'client': client
    }

    return render(request, 'edit/editClient.html', context)

@login_required(login_url='/login') 
@company_ownership_required(model_name="Alert", id_field="Client_id")
def editAlert(request, alert_id):

    alert = Alert.objects.select_related('agent').get(id=alert_id)  # Ya validado en el decorador

    if request.method == 'POST':

        alert_fields = ['name_client', 'phone_number', 'datetime', 'content' ]

        # Limpiar los campos 
        cleaned_alert_data = clean_fields_to_null(request, alert_fields)

        Alert.objects.filter(id=alert_id).update(
                name_client=cleaned_alert_data['name_client'],
                phone_number=cleaned_alert_data['phone_number'],
                datetime=cleaned_alert_data['datetime'],
                content=cleaned_alert_data['content']
            )
        return redirect('alert')

    return render(request, 'edit/editAlert.html', {'editAlert':alert} )
