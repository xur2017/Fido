from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import Pet, Picture
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views import generic
from rest_framework import generics
from django.conf import settings
from django import forms
from django.urls import reverse, reverse_lazy

# Create your views here.
def index(request):
    return render(request, 'pet/index.html')

class PetProfileView(generic.DetailView):
    context_object_name = 'pet'
    model = Pet
    template_name = 'pet/pet_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        petId = self.kwargs.get('pk')
        context['picture'] = Picture.objects.filter(pet_id=petId)
        return context

#############################################################################
# Pet View Functions:
# View for all pet information, including pictures
#############################################################################
#view pet, this will send all Pet info for /pet/<id> as context
#it will also send all pictures associated with that pet
class PetDetailView(generic.DetailView):
    context_object_name = 'pet'
    model = Pet
    template_name = 'pet/petdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        petId = self.kwargs.get('pk')
        context['picture'] = Picture.objects.filter(pet_id=petId)
        return context

def petDetail(request, pk):
    return PetDetailView.as_view()(request)

class PetListView(ListView):
    model = Pet
    #paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#############################################################################
# Pet Image Functions:
# Create and View for Pet Pictures
#############################################################################
#View for Profile Pictures only
class PetImageView(generic.DetailView):
    model = Picture
    template_name = 'pet/petdetail.html'

#CreateView for Pet Images
class PetImageCreate(CreateView):
    model = Picture
    fields = ['description', 'photo']

    def form_valid(self, form):
        petId = self.kwargs.get('pk')
        Pet.objects
        pet = Pet(id=petId)
        form.instance.pet = pet
        return super(PetImageCreate, self).form_valid(form)

#############################################################################
# Create Pet Functions:
# createPet calls PetCreate to use CreateView
#############################################################################

#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'status', 'description']

    def get_form(self, form_class=None):
        form = super(PetCreate, self).get_form(form_class)
        form.fields['description'].widget = forms.Textarea()
        return form

    #if form is valid, add shelter ID to pet
    def form_valid(self, form):
        result = super(PetCreate, self).form_valid(form)
        if self.request.user != 'AnonymousUser':
            self.object.users.add(self.request.user.id)
        return result

def createPet(request):
    if request.content_type == 'application/json':
        return PetCreate.as_view()(request)
    else:
        if request.user.is_authenticated:
            if request.user.user_type == 'S':
                return PetCreate.as_view()(request)
            else:
                output = 'You must be a Shelter user to create a pet!<br>'
                return HttpResponse(output)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

