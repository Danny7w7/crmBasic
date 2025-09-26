
# Django core libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Application-specific imports
from app.models import *

from django.shortcuts import render
from .decoratorsCompany import *

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Substr
from django.shortcuts import render
from datetime import datetime, date
import json

# Application-specific imports
from app.models import *

@login_required(login_url='/login')    
@company_ownership_required_sinURL 
def index(request):
    
    roleAuditar = ['S', 'C', 'AU']
    company_id = request.company_id

    if request.user.is_superuser:
        alert = Alert.objects.select_related('agent', 'company','client').annotate(
            truncated_contect=Substr('content', 1, 20))    
    elif request.user.role in roleAuditar:
        alert = Alert.objects.select_related('agent', 'company','client').annotate(
            truncated_contect=Substr('content', 1, 20)).filter(is_active=True, company=company_id)
    elif request.user.role == 'Admin':
        alert = Alert.objects.select_related('agent', 'company','client').annotate(
            truncated_contect=Substr('content', 1, 20)).filter(company=company_id)
    elif request.user.role == 'A':
        alert = Alert.objects.select_related('agent', 'company','client').annotate(
            truncated_contect=Substr('content', 1, 20)).filter(agent=request.user.id, is_active=True, company=company_id)
    
    # Convertir alertas a formato de eventos para FullCalendar
    events = []
    for alertClient in alert:
        # Combinar fecha y hora si ambos campos existen
        if hasattr(alertClient, 'time') and alertClient.time:           
            
            # Verificar si datetime es un objeto datetime o date
            if isinstance(alertClient.datetime, datetime):
                alert_date = alertClient.datetime.date()
            elif isinstance(alertClient.datetime, date):
                alert_date = alertClient.datetime
            else:
                # Fallback: intentar convertir a date
                alert_date = alertClient.datetime
                
            alert_time = alertClient.time
            combined_datetime = datetime.combine(alert_date, alert_time)
            start_time = combined_datetime.isoformat()
        else:
            # Usar solo el datetime original
            if hasattr(alertClient.datetime, 'isoformat'):
                start_time = alertClient.datetime.isoformat()
            else:               
                if isinstance(alertClient.datetime, date):
                    start_time = datetime.combine(alertClient.datetime, datetime.min.time()).isoformat()
                else:
                    start_time = str(alertClient.datetime)
            
        event = {
            'id': alertClient.id,
            'title': f"{alertClient.client.full_name} - {alertClient.truncated_contect}",
            'start': start_time,
            'description': f"Agent: {alertClient.agent.first_name} {alertClient.agent.last_name}",
            'completed': alertClient.completed,
            'extendedProps': {
                'agent_name': f"{alertClient.agent.first_name} {alertClient.agent.last_name}",
                'client_name': alertClient.client.full_name,
                'client_phone': alertClient.client.phone_number,
                'content': alertClient.content,
                'is_active': alertClient.is_active,
                'company_name': alertClient.company.company_name if hasattr(alertClient, 'company') else '',
                'time': alertClient.time.strftime('%H:%M') if hasattr(alertClient, 'time') and alertClient.time else '',
                'datetime': alertClient.datetime.strftime('%Y-%m-%d %H:%M') if hasattr(alertClient.datetime, 'strftime') else str(alertClient.datetime),
                'edit_url': f"/editAlert/{alertClient.id}/", 
                'toggle_url': f"/toggleAlert/{alertClient.id}/",
                'asistio_url': f"/asistio/{alertClient.id}/" 
            }
        }
        
        # Agregar color basado en el estado
        if hasattr(alertClient, 'completed'):
            event['backgroundColor'] = '#28a745' if alertClient.completed else '#dc3545'
            event['borderColor'] = '#28a745' if alertClient.completed else '#dc3545'
        
        events.append(event)
    
    context = {
        'alertC': alert,
        'events_json': json.dumps(events),
        'user_role': request.user.role,
        'is_superuser': request.user.is_superuser
    }
    
    return render(request, 'dashboard/index.html', context)


def asistio(request, alert_id):

    Alert.objects.filter(id = alert_id).update(
        completed = True
    )

    return redirect('index')








