from django.db import models

# Create your models here.

class UserType(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class User(models.Model):
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE)
    
    email_address = models.CharField(max_length=40, blank=True)
    name = models.CharField(max_length=40, blank=True)
    phone_number = models.CharField(max_length=40, blank=True)
    username = models.CharField(max_length=40, blank=True)
    password = models.CharField(max_length=40, blank=True)
    verification = models.CharField(max_length=40, blank=True)
    street_number = models.CharField(max_length=40, blank=True)
    street_name = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=40, blank=True)
    zip = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.email_address
    
class PetType(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class Breed(models.Model):
    pet_type = models.ForeignKey('PetType', on_delete=models.CASCADE)

    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class Disposition(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description
    
class Availability(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class Pet(models.Model):
    pet_type = models.ForeignKey('PetType', on_delete=models.CASCADE)
    breed = models.ForeignKey('Breed', on_delete=models.CASCADE)
    disposition = models.ForeignKey('Disposition', on_delete=models.CASCADE)
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE)
    
    users = models.ManyToManyField(User)
    
    name = models.CharField(max_length=40, blank=True)
    age = models.FloatField(null=True, blank=True) 
    sex = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(blank=True)
    
    def __str__(self):
        return self.description

    

    