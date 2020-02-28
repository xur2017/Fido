from django.contrib import admin

# Register your models here.
from .models import UserType, CustomUser, Picture, Pet, Status

admin.site.register(CustomUser)
admin.site.register(Pet)
admin.site.register(Picture)
admin.site.register(Status)
