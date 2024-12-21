from django.contrib import admin
from .models import CustomUser, Hobby

admin.site.register(CustomUser)
admin.site.register(Hobby)
