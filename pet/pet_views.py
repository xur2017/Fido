from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import Pet
from django.views.generic.edit import CreateView
from django.views import generic
from rest_framework import generics
from django.conf import settings
from django import forms

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
    test = request
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

