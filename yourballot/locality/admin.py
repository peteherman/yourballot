from django.contrib import admin

# Register your models here.
from yourballot.locality.models import PoliticalLocality, ZipcodeLocality

admin.site.register(PoliticalLocality)
admin.site.register(ZipcodeLocality)
