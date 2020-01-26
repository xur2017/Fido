from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import Pet
from django.views.generic.edit import CreateView
from django.views import generic
from rest_framework import generics

# Create your views here.
def index(request):
    return render(request, 'pet/index.html')

#view pet, this will send all Pet info for /pet/<id> as context
class PetDetailView(generic.DetailView):
    model = Pet
    template_name = 'pet/petdetail.html'

#############################################################################
# Create Pet Functions:
# createPet calls PetCreate to use CreateView
#############################################################################

#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'status', 'description',
              'picture']

    #if form is valid, add shelter ID to pet
    def form_valid(self, form):
        result = super(PetCreate, self).form_valid(form)
        if self.request.user != 'AnonymousUser':
            self.object.users.add(self.request.user.id)
        return result

def createPet(request):
    test = request
    #TO DO: Add check for is authenticated ANDALSO to make sure is a shelter
    if request.content_type == 'application/json':
        return PetCreate.as_view()(request)
    else:
        return PetCreate.as_view()(request)
