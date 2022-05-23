from django.contrib import admin

# Register your models here.
from authapp.models import HabrUser, HabrProfile

admin.site.register(HabrUser)
admin.site.register(HabrProfile)
