# Standard Python libraries
from django.http import HttpResponse
from django.db.models import F

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render 

# Application-specific imports
from app.models import *
from ..decoratorsCompany import *

@login_required(login_url='/login') 
@superuserRequired
def formCreateCompanies(request):

    companies = Companies.objects.exclude(id = 1)

    if request.method == 'POST':
        owner = request.POST.get('owner').upper()
        name = request.POST.get('name').upper()
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        try:
            company = Companies.objects.create(
                owner=owner,
                company_name=name, 
                phone_company=phone,
                company_email=email,
            )

            context = {
                'msg':f'Companies {company.company_name} creado con éxito.',
                'companies':companies,
                'type':'good'
            }

            return render(request, 'forms/formCreateCompanies.html', context)

        except Exception as e:
            return HttpResponse(str(e))
    
    context = {
        'companies':companies
    }
            
    return render(request, 'forms/formCreateCompanies.html', context)

@login_required(login_url='/login') 
@superuserRequired
def editCompanies(request, company_id):
    # Obtener el usuario a editar o devolver un 404 si no existe
    company = get_object_or_404(Companies, id=company_id)

    if request.method == 'POST':
        # Recuperar los datos del formulario

        owner = request.POST.get('owner', company.owner)
        name = request.POST.get('name', company.company_name)
        phone = request.POST.get('phone', company.phone_company)
        email = request.POST.get('email', company.company_email)
        is_active = request.POST.get('is_active', company.is_active)

        # Actualizar los datos del usuario
        company.owner = owner
        company.company_name = name
        company.phone_company = phone
        company.company_email = email
        company.is_active = is_active

        # Guardar los cambios
        company.save()

        # Redirigir a otra vista o mostrar un mensaje de éxito
        return redirect('formCreateCompanies')  

    # Renderizar el formulario con los datos actuales del usuario
    context = {'company': company}
    return render(request, 'edit/editCompanies.html', context)

@login_required(login_url='/login') 
@superuserRequired
def toggleCompanies(request, company_id):
    # Obtener el cliente por su ID
    company = get_object_or_404(Companies, id=company_id)

    users = Users.objects.filter(company=company)
    users.update(is_active=~F('is_active'))
    
    # Cambiar el estado de is_active (True a False o viceversa)
    company.is_active = not company.is_active
    company.save()  # Guardar los cambios en la base de datos
    
    # Redirigir de nuevo a la página actual con un parámetro de éxito
    return redirect('formCreateCompanies')

def validatePhoneNumber(phoneNumber):
    """
    Valida y formatea un número de teléfono según las siguientes reglas:
    - Debe tener 10 u 11 dígitos.
    - Si tiene 11 dígitos, el primero debe ser '1'.
    - Si tiene 10 dígitos, se agrega '1' al inicio.
    - Si tiene más de 11 dígitos y no comienza con '1', se considera inválido.
    - En cualquier otro caso (menos de 10 dígitos), se considera inválido.
    """
    cleanNumber = ''.join(filter(str.isdigit, str(phoneNumber)))
    length = len(cleanNumber)

    if length == 10:
        return '1' + cleanNumber
    elif length == 11:
        if cleanNumber.startswith('1'):
            return cleanNumber
        else:
            return False
    elif length > 11:
        if cleanNumber.startswith('1'):
            return cleanNumber
        else:
            return False
    else:
        return False

