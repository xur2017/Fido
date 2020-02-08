from .models import Pet
import django_filters

class PetFilter(django_filters.FilterSet):
    class Meta:
        model = Pet
        fields = {'name': ['icontains'], 
                  'pet_type': ['exact'],
                  'age': ['gte', 'lte'],
                  'breed': ['exact'],
                  'sex': ['exact'], }