from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Companies(models.Model):
    owner = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    phone_company = models.BigIntegerField()
    company_email = models.EmailField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'companies'

class Users(AbstractUser):

    ROLES_CHOICES = (
        ('A', 'Agent'),
        ('S', 'Supervisor'),
        ('C', 'Customer'),
        ('SUPP', 'Supplementary'),
        ('AU', 'Auditor'),
        ('TV', 'Tv'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES_CHOICES)
    # Sobrescribimos solo el campo email
    email = models.EmailField(
        blank=True, 
        null=True,
        unique=False
    )
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'users'
        
    def _str_(self):
        return self.username
    
    
    def formatted_phone_number(self):
        if self.assigned_phone and self.assigned_phone.phone_number:
            phone_str = str(self.assigned_phone.phone_number)
            formatted = f"+{phone_str[0]} ({phone_str[1:4]}) {phone_str[4:7]} {phone_str[7:]}"
            return formatted
        return None
    
    def formatted_phone_number_whatsapp(self):
        if self.assigned_phone_whatsapp and self.assigned_phone_whatsapp.phone_number:
            phone_str = str(self.assigned_phone_whatsapp.phone_number)
            formatted = f"+{phone_str[0]} ({phone_str[1:4]}) {phone_str[4:7]} {phone_str[7:]}"
            return formatted
        return None
    
class UserPreference(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    darkMode = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_preference'

class Motivation(models.Model):
    content = models.TextField()

    class Meta:
        db_table = 'motivation'

class Clients(models.Model):
    agent = models.ForeignKey(Users, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True)
    cod_number =  models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    email = models.EmailField()
    is_active = models.BooleanField(default=True)  
    description = models.TextField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

    class Meta:
        db_table = 'clients'

class Alert(models.Model):
    agent = models.ForeignKey(Users, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    datetime = models.DateField()
    time = models.TimeField()
    content = models.TextField(blank=True)
    completed = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

    class Meta:
        db_table = 'alert'
