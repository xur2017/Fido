from .models import Pet
from localflavor.us.us_states import US_STATES
import django_filters

class PetFilter(django_filters.FilterSet):
    #https://stackoverflow.com/questions/54062160/django-filters-custom-method-field-name
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Name")
    pet_type = django_filters.ChoiceFilter(field_name='pet_type', choices=Pet.PET_TYPE_CHOICES, lookup_expr='exact', label="Pet Type")
    age = django_filters.NumberFilter(field_name='age', lookup_expr='gte', label="Age - Min")
    age2 = django_filters.NumberFilter(field_name='age', lookup_expr='lte', label="Age - Max")
    breed = django_filters.ChoiceFilter(field_name='breed', choices=Pet.BREED_CHOICES, lookup_expr='exact', label="Breed")
    sex = django_filters.ChoiceFilter(field_name="sex", choices=Pet.SEX_CHOICES, lookup_expr='exact', label="Sex")
    disposition = django_filters.ChoiceFilter(field_name="disposition", choices=Pet.DISPOSITION_CHOICES, lookup_expr="exact", label="Disposition")
    updated_at = django_filters.CharFilter(field_name="updated_at", lookup_expr='gte', label="Last Updated (YYYY-MM-DD) - Min")
    updated_at2 = django_filters.CharFilter(field_name="updated_at", lookup_expr='lte', label="Last Updated (YYYY-MM-DD) - Max")
    users_state = django_filters.ChoiceFilter(field_name="users__state", choices=US_STATES, lookup_expr='exact', label="Shelter State", method='filter_state')
    users_name = django_filters.CharFilter(field_name="users__first_name", lookup_expr='icontains', label="Shelter Name")
    users_city = django_filters.CharFilter(field_name="users__city", lookup_expr='icontains', label="Shelter City")

    def filter_state(self, queryset, name, value):
        # only pull back state of Shelter
        queryset = queryset.filter(users__state=value,users__user_type='S')
        return queryset

    class Meta:
        model = Pet
        fields = ['name',
                  'pet_type',
                  'age',
                  'breed',
                  'sex',
                  'disposition',
                  'updated_at',
                  'users__first_name',
                  'users__state']

        def __init__(self, *args, **kwargs):
            super(PetFilter, self).__init__(*args, **kwargs)
            self.fields['state'].queryset = Pet.objects.filter(users__user_type='S')
