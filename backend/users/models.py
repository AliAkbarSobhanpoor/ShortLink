import random
import datetime
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from rest_framework import serializers
from django.db.models import Q
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def __check_duplicate(self, email, phone_number):
        if email and self.model.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError("email already exist")
        
        if phone_number and self.model.objects.filter(phone_number=phone_number, is_active=True).exists():
            raise serializers.ValidationError("PhoneNumber already exist")
        
            
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("user most have either email or password")
        
        if email:
            email = self.normalize_email(email)
        
        self.__check_duplicate(email=email, phone_number=phone_number)
        
        extra_fields.setdefault('is_active', False)

        random_code = random.randint(100_000, 999_999)
        
        if settings.DEBUG:
            print(random_code)
        extra_fields.setdefault('verification_code', str(random_code))
        extra_fields.setdefault('verification_expiry', datetime.datetime.now() + datetime.timedelta(minutes=5))
        
        query = Q(is_active=False)
        
        if email:
            query &= Q(email=email)

        if phone_number:
            query &= Q(phone_number=phone_number)

        user = User.objects.filter(query).first()
        if user:
            return user
        else:
            user: User = self.model(
                email=email, 
                phone_number=phone_number,
                **extra_fields
            )
            
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            
            user.save(using=self._db) # if you use multiple database this is required.
            return user
    
    
    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        if not password:
            raise ValueError("super user most have email")
        
        self.__check_duplicate(email=email, phone_number=phone_number)
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('verification_code', None)
        extra_fields.setdefault('verification_expiary', None)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(verbose_name=_("phone number"), max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name=_("email"), unique=True, null=True, blank=True)
    
    password = models.CharField(_("password"), max_length=128, blank=True, null=True)
    
    is_active = models.BooleanField(verbose_name=_("is active"), default=False)
    verification_code = models.CharField(verbose_name=_("verification code"), max_length=6, null=True, blank=True) # use for both activation and login.
    verification_expiry = models.DateTimeField(verbose_name=_("verification code expiry"), null=True, blank=True)
    
    date_joined = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=_("last login"), null=True, blank=True)
    
    is_staff = models.BooleanField(verbose_name=_("staff"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("superuser"), default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def active_user(self, verification_code, **extra_fields):
        if self.is_active == False and self.verification_expiry > timezone.now():
            self.is_active = True
            self.verification_code = None
            self.verification_expiary = None
            self.save()
            return self
        else:
            raise serializers.ValidationError("expary date has existed")
    
    def __str__(self):
        return self.email if self.email else self.phone_number