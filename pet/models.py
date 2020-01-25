from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserType(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class CustomUser(AbstractUser):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    #user_type = models.ForeignKey('UserType', on_delete=models.CASCADE)
    USER_TYPE_CHOICES = [
        ('S', 'Shelter'),
        ('P', 'Pet Parent')
    ]
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
        default='S'
    )
    #email_address = models.CharField(max_length=40, blank=True)
    #name = models.CharField(max_length=40, blank=True)
    phone_number = models.CharField(max_length=40, blank=True)
    #username = models.CharField(max_length=40, blank=True)
    #password = models.CharField(max_length=40, blank=True)
    street_number = models.CharField(max_length=40, blank=True)
    street_name = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=40, blank=True)
    zip = models.CharField(max_length=40, blank=True)
    document = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return "/user/%i/" % self.id
    
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

class Picture(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE)

    description = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/', blank=True)
    
    def __str__(self):
        return self.description
        
class Pet(models.Model):
    #https://docs.djangoproject.com/en/3.0/ref/models/fields/#afield-choices

    #Choices for Pet Types:
    #pet_type = models.ForeignKey('PetType', on_delete=models.CASCADE)
    DOG = 'D'
    CAT = 'C'
    OTHER = 'O'

    PET_TYPE_CHOICES = [
        (DOG, 'Dog'),
        (CAT, 'Cat'),
        (OTHER, 'Other')
    ]

    pet_type = models.CharField(
        max_length=2,
        choices = PET_TYPE_CHOICES,
        default= DOG
    )

    #Choices for Breeds
    #breed = models.ForeignKey('Breed', on_delete=models.CASCADE)
    BREED_CHOICES = [
        ('B', 'Beagle'),
        ('FB', 'French Bulldog'),
        ('GR', 'Golden Retriever'),
        ('GS', 'German Shepard'),
        ('L', 'Laborador')

    ]

    breed = models.CharField(
        max_length=2,
        choices=BREED_CHOICES,
        default='B'
    )

    #Choices for Disposition
    #disposition = models.ForeignKey('Disposition', on_delete=models.CASCADE)
    DISPOSITION_CHOICES = [
        ('C', 'Good with Children'),
        ('OA', 'Good with Other Animals'),
        ('L', 'Animal must be leashed at all times'),
        ('NA', 'Not Applicable')
    ]

    disposition = models.CharField(
        max_length=2,
        choices=DISPOSITION_CHOICES,
        default="NA"
    )

    #Choices for Availability
    #availability = models.ForeignKey('Availability', on_delete=models.CASCADE)

    AVAILABLE = 'A'
    NOT_AVAILABLE = 'NA'
    PENDING = 'P'
    ADOPTED = 'AD'

    AVAILABILITY_CHOICES = [
        (AVAILABLE, 'Available'),
        (NOT_AVAILABLE, 'Not Available'),
        (PENDING, 'Pending'),
        (ADOPTED, 'Adopted')
    ]
    availability = models.CharField(
        max_length=2,
        choices = AVAILABILITY_CHOICES,
        default = AVAILABLE
    )


    users = models.ManyToManyField(CustomUser)
    
    name = models.CharField(max_length=40)
    age = models.FloatField(null=True, blank=True) 
    sex = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/pet/%i/" % self.id
    

    