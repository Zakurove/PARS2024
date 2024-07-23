# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models
# from django.utils.translation import gettext_lazy as _

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError(_('The Email field must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))

#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     created_at = models.DateTimeField(auto_now_add=True)
#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    profile_picture = models.ImageField(upload_to='static/user/img', default='default_icon.jpeg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email