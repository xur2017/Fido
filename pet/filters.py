from .models import Pet
import django_filters

class PetFilter(django_filters.FilterSet):
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'age', 'breed', 'sex', ]