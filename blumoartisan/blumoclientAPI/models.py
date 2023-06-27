from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime


# Create your models here.

class ClientUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, password=None):
        
        if not email:
            raise ValueError('Users must have email address!')
        
        if not phone_number:
            raise ValueError('Phone number must be included!')
        
        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            first_name = first_name,
            last_name =last_name,
            password=password
            
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone_number, first_name, last_name, password=None):
        
        user = self.create_superuser(
            email,
            phone_number,
            first_name,
            last_name,
            password=password,
               
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
        
        
class ClientUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField(blank=True)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(default=0)
    
    objects = ClientUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_out_of_credits(self):
        "Is the user out  of credits?"
        return self.credits > 0

    @property
    def has_sufficient_credits(self, cost):
        return self.credits - cost >= 0

    @property
    def linkedin_signed_in(self):

        return bool(self.linkedin_token) and self.expiry_date > timezone.now()