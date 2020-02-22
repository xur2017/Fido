from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import USStateField
#https://django-localflavor.readthedocs.io/en/latest/#

# Create your models here.

class UserType(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
class CustomUser(AbstractUser):
    #Username, password, first name, last name, email will all be created from User, do not need to be defined here
    USER_TYPE_CHOICES = [
        ('S', 'Shelter'),
        ('P', 'Pet Parent')
    ]

    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default='S')
    phone_number = models.CharField(max_length=40, blank=True)
    street_number = models.CharField(max_length=40, blank=True)
    street_name = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = USStateField(null=False, blank=False)
    zip = models.CharField(max_length=40, blank=True)
    document = models.FileField(upload_to='documents/', blank=True)
    profilePic = models.ImageField(upload_to='userPics/', blank=True)

    #Automatically track date
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return "/user/%i/" % self.id

class Picture(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, default=None)

    description = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return "/pic/%i" % self.id

class Pet(models.Model):
    #https://docs.djangoproject.com/en/3.0/ref/models/fields/#afield-choices
    # Choices for Availability
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
    # Choices for Sex
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other/Unknown')
    ]
    #Choices for Pet Types:
    DOG = 'D'
    CAT = 'C'
    OTHER = 'O'

    PET_TYPE_CHOICES = [
        (DOG, 'Dog'),
        (CAT, 'Cat'),
        (OTHER, 'Other')
    ]
    # Choices for Disposition
    DISPOSITION_CHOICES = [
        ('C', 'Good with Children'),
        ('OA', 'Good with Other Animals'),
        ('L', 'Animal must be leashed at all times'),
        ('NA', 'Not Applicable')
    ]
    #Choices for Breeds
    BREED_CHOICES = [
        ('B', 'Beagle'),
        ('BX', 'Boxers'),
        ('FB', 'French Bulldog'),
        ('GR', 'Golden Retriever'),
        ('GS', 'German Shepard'),
        ('L', 'Laborador'),
        ('PT', 'Pointers'),
        ('P', 'Poodle'),
        ('R', 'Rottweiler'),
        ('Y','Yorkshire Terrier'),

        ('A', 'Abyssinian'),
        ('BN', 'Bengal'),
        ('DR', 'Devon Rex'),
        ('H', 'Himalayan'),
        ('MC', 'Maine Coon'),
        ('PR', 'Persian'),
        ('RD', 'Ragdoll'),
        ('SH', 'Shorthairs'),
        ('S', 'Siamese'),
        ('SP', 'Sphynx'),

        ('M', 'Mixed Breed'),
        ('O', 'Other'),
        ('UN', 'Unknown'),
    ]

    #Identifiers
    availability = models.CharField(max_length=2, choices=AVAILABILITY_CHOICES, default=AVAILABLE)
    breed = models.CharField(max_length=2, choices=BREED_CHOICES, default='B')
    disposition = models.CharField(max_length=2, choices=DISPOSITION_CHOICES, default='N/A')
    pet_type = models.CharField(max_length=2, choices=PET_TYPE_CHOICES, default=DOG)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=MALE)
    users = models.ManyToManyField(CustomUser)

    #Required name and age
    name = models.CharField(max_length=40)
    age = models.FloatField(null=True, blank=True)

    #Optional status and description
    status = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=200, blank=True)

    #Automatically track date
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/pet_profile/%i/" % self.id
    

