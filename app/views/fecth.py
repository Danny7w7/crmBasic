# Standard Python libraries
import json
import requests

# Django utilities
from django.http import JsonResponse

# Django core libraries
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Application-specific imports
from app.models import *


#fech para llenado de datos en formCreateShipping
def findClient(request):
  search = request.GET.get('search', '')
  remitentes = Clients.objects.filter(full_name__icontains=search, is_active=True).values('id', 'full_name')[:10]
  data = list(remitentes)
  print('AQUI VA LA DATA')
  print(data)
  return JsonResponse({'data': data})


@login_required(login_url='/login') 
def searchClientData(request):
  client_id = request.GET.get('id')
  try:
    client = Clients.objects.get(id=client_id, is_active=True)
    data = {
      'address': client.address,
      'phone_number': client.phone_number,
      'id': client.id
    }
    return JsonResponse({'success': True, 'data': data})
  except Clients.DoesNotExist:
    return JsonResponse({'success': False, 'error': 'No se encontró el remitente'})
