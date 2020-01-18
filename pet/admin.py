from django.contrib import admin

# Register your models here.
from .models import UserType, User, PetType, Breed, Disposition, Availability, Pet

admin.site.register(UserType)
admin.site.register(User)
admin.site.register(PetType)
admin.site.register(Breed)
admin.site.register(Disposition)
admin.site.register(Availability)
admin.site.register(Pet)