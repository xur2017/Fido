from django.contrib import admin

# Register your models here.
from .models import UserType, CustomUser, PetType, Breed, Disposition, Availability, Picture, Pet

admin.site.register(UserType)
admin.site.register(CustomUser)
admin.site.register(PetType)
admin.site.register(Breed)
admin.site.register(Disposition)
admin.site.register(Availability)
admin.site.register(Pet)
admin.site.register(Picture)
