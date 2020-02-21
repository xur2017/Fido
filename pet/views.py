from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import Pet
from django.views.generic.edit import CreateView
from django.views import generic
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'pet/index.html')

#view pet, this will send all Pet info for /pet/<id> as context
class PetDetailView(generic.DetailView):
    model = Pet
    template_name = 'pet/petdetail.html'

#############################################################################
# Create Pet Functions:
#
#############################################################################


#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'status', 'description']

def createPet(request):
    return PetCreate.as_view()(request)

def view_404(request, exception=None):
	messages.add_message(request,messages.ERROR,
		'You do not have the correct level of permission and/or access.',fail_silently=True)
	return HttpResponseRedirect('/')