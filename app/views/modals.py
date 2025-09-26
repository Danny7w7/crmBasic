from django.http import JsonResponse
from app.models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login') 
def getRemitterDetail(request, id):
    try:
        client = Clients.objects.get(id=id)
        data = {
            'full_name': client.full_name,
            'address': client.address,
            'city': client.city,
            'country': client.country,
            'cod_number': client.cod_number,
            'phone_number': str(client.phone_number),
            'email': client.email,
            'created_at': client.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        return JsonResponse({'success': True, 'data': data})
    except Clients.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Remitter no encontrado'})
