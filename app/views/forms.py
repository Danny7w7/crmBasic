#libreria de paises
from django.shortcuts import render

# Django core libraries
from django.contrib.auth.decorators import login_required

# Application-specific imports
from app.forms import *
from app.models import *
from .decoratorsCompany import *


# Vista para crear cliente
@login_required(login_url='/login') 
@company_ownership_required_sinURL
def formCreateClients(request):

    if request.user.is_superuser:
        clientsTable = Clients.objects.all()
    else:
        clientsTable = Clients.objects.filter(is_active = True)

    error_message = request.session.pop('client_error', None)

    if request.method == 'POST':

        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.agent = request.user
            client.is_active = True
            client.company = request.user.company

            # Convertir a mayúsculas
            client.full_name = client.full_name.upper()
            client.address = client.address.upper()
            client.city = client.city.upper()
            client.country = client.country.upper()

            client.save()
         
            # Responder con éxito y la URL de redirección
            return redirect('formCreateAlert')
        else:
            return render(request, 'forms/formCreateClients.html', {'error_message': form.errors})
        
    context = {
        'client_error': error_message,
        'clientsTable': clientsTable
    }    
    
    return render(request, 'forms/formCreateClients.html', context)

@login_required(login_url='/login') 
@company_ownership_required_sinURL
def formCreateAlert(request):

    if request.method == 'POST':

        idClient = request.POST.get('idClient')
        client = Clients.objects.filter(id=idClient).first()

        formClient = AlertForm(request.POST)
        if formClient.is_valid():
            alert = formClient.save(commit=False)
            alert.agent = request.user
            alert.client = client
            alert.is_active = True
            alert.company = request.user.company
            alert.save()
            return redirect('index',)  # Cambia a tu página de éxito

    return render(request, 'forms/formCreateAlert.html')

