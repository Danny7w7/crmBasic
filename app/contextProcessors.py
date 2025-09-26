from .models import UserPreference, Companies

def themeMode(request):
    try:
        userPreference = UserPreference.objects.get(user_id=request.user.id)
    except:
        userPreference = None
    return {
        'userPreference': userPreference,
    }

def company(request):
    try:
        company = Companies.objects.get(id=request.user.company.id)
    except:
        company = None
    return {'nameCompany': company}

