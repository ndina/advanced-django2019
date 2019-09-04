from django.contrib import admin
from .models import Stuff, StuffStockDetails
# Register your models here.

admin.site.register(Stuff)
admin.site.register(StuffStockDetails)
