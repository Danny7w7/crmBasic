# Django core libraries
from django.shortcuts import get_object_or_404, redirect
 
# Application-specific imports
from app.models import *

def toggleAlert(request, alert_id):
    # Obtener el cliente por su ID
    alert = get_object_or_404(Alert, id=alert_id)
    
    # Cambiar el estado de is_active (True a False o viceversa)
    alert.is_active = not alert.is_active
    alert.save()  # Guardar los cambios en la base de datos
    
    # Redirigir de nuevo a la página actual con un parámetro de éxito
    return redirect('alert')

def toggleClients(request, Client_id):   
    
    # Obtener el cliente por su ID
    client = get_object_or_404(Clients, id=Client_id)
    
    # Cambiar el estado de is_active (True a False o viceversa)
    client.is_active = not client.is_active
    client.save()  # Guardar los cambios en la base de datos
    
    # Redirigir de nuevo a la página actual con un parámetro de éxito
    return redirect('formCreateClients')


