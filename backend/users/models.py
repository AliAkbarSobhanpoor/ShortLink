from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(verbose_name=_("phone number"), max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name=_("email"), unique=True, null=True, blank=True)
    
    password = models.CharField(_("password"), max_length=128, blank=True, null=True)
    
    is_active = models.BooleanField(verbose_name=_("is active"), default=False)
    verification_code = models.CharField(verbose_name=_("verification code"), max_length=6, null=True, blank=True) # use for both activation and login.
    verification_expiry = models.DateTimeField(verbose_name=_("verification code expiry"), null=True, blank=True)
    
    date_joined = models.DateTimeField(verbose_name=_("date joined"))
    last_login = models.DateTimeField(verbose_name=_("last login"), null=True, blank=True)
    
    is_staff = models.BooleanField(verbose_name=_("staff"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("superuser"), default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    manager = UserManager()
    
    def __str__(self):
        return self.email if self.email else self.phone_number
    
    
    
'''
CUSTOM USERMANAGER FOR CREATE USER OR SUPERUSER

CUSTOM BACKEND FOR CURRECT LOGIN IN TEHE BACKEND. IF YOU DONT NEED DJANGO BACKEND THEN YOU CAN REMOVE THE CREATION OF THE CUSTOM BACKEND.

'''