from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from .constants import PRODUCT_TYPE, SERVICE_TYPE

from midterm.settings import AUTH_USER_MODEL


#
# class MainUserManager(BaseUserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not username:
#             raise ValueError('The given username must be set')
#         email = self.normalize_email(email)
#         username = self.model.normalize_username(username)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_guest(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         extra_fields.setdefault('is_guest', True)
#         return self._create_user(username, email, password, **extra_fields)
#
#     def create_store_admin(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         extra_fields.setdefault('is_guest', False)
#         extra_fields.setdefault('is_store_admin', False)
#         return self._create_user(username, email, password, **extra_fields)
#
#     def create_superuser(self, username, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(username, email, password, **extra_fields)
#
#
# class MainUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     is_store_admin = models.BooleanField(default=False)
#     is_guest = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#
#     objects = MainUserManager()
#
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.CharField(u'Аватар пользователя', max_length=200)
    address = models.CharField(u'Адрес пользователя', max_length=200)
    bio = models.TextField(u'Биография пользователя', null=True, blank=True)

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __str__(self):
        return self.user.username


class ProductServiceBase(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(ProductServiceBase):
    size = models.IntegerField()
    type = models.IntegerField(choices=PRODUCT_TYPE, default=0)
    existence = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Service(ProductServiceBase):
    approximate_duration = models.IntegerField()
    service_type = models.IntegerField(choices=SERVICE_TYPE, default=0)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
