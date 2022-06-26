import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        if other_fields.get('is_superuser') is not True:
            return ValueError('Superuser must have assigned "is_superuser" option to True')
            
        if other_fields.get('is_staff') is not True:
            return ValueError('Superuser must have assigned "is_staff" option to True')
        
        return self.create_user(email, first_name, last_name, password, **other_fields)
    
    def create_user(self, email, first_name, last_name, password, **other_fields):

        if not email:
            return ValueError('You must provide email address!')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_('Unique identifier')
    )
    email = models.EmailField(
        help_text=_("Address Email"),
        unique=True
    )

    first_name = models.CharField(
        max_length=50, 
        help_text=_("First Name")
        )

    last_name = models.CharField(
        max_length=50, 
        help_text=_('Last Name')
        )
    
    created_at = models.DateTimeField(
        help_text=_('Account Created At'),
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        help_text=_('Last time updated'),
        auto_now=True,
        editable=False
    )
    
    is_staff = models.BooleanField(
        help_text=_('User is staff'),
        default=False
    )

    is_superuser = models.BooleanField(
        help_text=_('User is superuser'),
        default=False
    )

    is_active = models.BooleanField(
        help_text=_('User is active'),
        default=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()