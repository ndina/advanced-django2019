from django.contrib import admin
from .models import UserProfile, Product, Service

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Service)


