from django.contrib import admin

# Register your models here.
from .models import UserType, CustomUser, Picture, Pet

admin.site.register(CustomUser)
admin.site.register(Pet)
admin.site.register(Picture)
