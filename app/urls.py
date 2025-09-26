"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import table, toggles, edits, forms, modals, auth, index, fecth
from .views.users import users, companies
from .views import utils 


urlpatterns = [
    #<---------------------------Auth--------------------------->
    path('login/', auth.login_, name='login'),
    path('logout/', auth.logout_, name='logout'),
    path('motivationalPhrase/', auth.motivationalPhrase, name='motivationalPhrase'),

    #<---------------------------DashBoard--------------------------->
    path('', index.index, name='index'), #Home

    #<---------------------------Client--------------------------->
    path('formCreateClients/', forms.formCreateClients, name='formCreateClients'), 
    path('toggleClients/<Client_id>/', toggles.toggleClients, name='toggleClients'),
    path('editClient/<client_id>/', edits.editClient, name='editClient'),

    #<---------------------------Alerts--------------------------->
    path('formCreateAlert/', forms.formCreateAlert, name='formCreateAlert'), 
    path('toggleAlert/<alert_id>/', toggles.toggleAlert, name='toggleAlert'),
    path('editAlert/<int:alert_id>/', edits.editAlert, name='editAlert'),

    #<---------------------------Users--------------------------->    
    path('formCreateUser/', users.formCreateUser, name='formCreateUser'),
    path('editUser/<user_id>', users.editUser, name='editUser'),
    path('toggleUser/<user_id>/', users.toggleUser, name='toggleUser'),

    #<---------------------------Company---------------------------> 
    path('formCreateCompanies/', companies.formCreateCompanies, name='formCreateCompanies'),
    path('editCompanies/<company_id>', companies.editCompanies, name='editCompanies'),
    path('toggleCompanies/<company_id>/', companies.toggleCompanies, name='toggleCompanies'),

    #<---------------------------Utils---------------------------> 
    path('toggleDarkMode/', utils.toggleDarkMode, name='toggleDarkMode'),
    path('getRemitterDetail/<int:id>/', modals.getRemitterDetail, name='getRemitterDetail'),
    path('findClient/', fecth.findClient, name='findClient'),
    path('searchClientData/', fecth.searchClientData, name='searchClientData'),
    path('asistio/<int:alert_id>/', index.asistio, name='asistio'),


]