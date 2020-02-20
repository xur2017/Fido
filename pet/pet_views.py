from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views import generic
from rest_framework import generics
from django.conf import settings
from django import forms
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, BadHeaderError
import feedparser

from .models import Pet, Picture
from .filters import PetFilter
from . import feeds
from .forms import EmailContactForm

# Create your views here.
def index(request):
    return render(request, 'pet/index.html')

def emailView(request):
    if request.method == 'GET':
        form = EmailContactForm()
    else:
        form = EmailContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            to_email = form.cleaned_data['to_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, 'admin@example.com', [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return redirect( 'http://' + request.get_host() + '/success' )
            return redirect( reverse_lazy('pet:success') )
    return render(request, "pet/email.html", {'form': form})

def successView(request):
    return HttpResponse('Success.')

class FavListView(ListView):
    model = Pet
    ordering = ['-updated_at']
    #paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Pet.objects.filter(users__pk = self.request.user.id)
        else:
            raise Http404

#############################################################################
# Pet Search Function:
# Returns a filter of pets per criteria
#############################################################################
def search(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET, queryset=pet_list)
    return render(request, 'pet/pet_filter.html', {'filter': pet_filter})

#############################################################################
# About Team related Functions:
# Returns page for team overview
#############################################################################
def about(request):
    return render(request, 'registration/about.html')

def services(request):
    return render(request, 'registration/services.html')

#def volunteer(request):
#    return render(request, 'registration/volunteer.html')

#############################################################################
# Pet View Functions:
# View for all pet information, including pictures
# For shelter, not allowed for pet parent
#############################################################################
#view pet, this will send all Pet info for /pet/<id> as context
#it will also send all pictures associated with that pet
class PetDetailView(generic.DetailView):
    context_object_name = 'pet'
    model = Pet
    template_name = 'pet/petdetail.html'

    def get_object(self, queryset=None, *args, **kwargs):
        if self.request.user.is_authenticated:
            obj = super(PetDetailView, self).get_object(*args, **kwargs)
            for u in obj.users.all():
                if u.id == self.request.user.id and u.user_type == 'S':
                    return obj
                else:
                    raise Http404
            raise Http404
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        petId = self.kwargs.get('pk')
        context['picture'] = Picture.objects.filter(pet_id=petId)
        return context

#This is for pet parents, not owner of pet profile
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
# Pet List Functions:
# For browse
#############################################################################
class PetListView(ListView):
    model = Pet
    ordering = ['-updated_at']
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

    def get_initial(self, queryset=None, *args, **kwargs):
        petId = self.kwargs.get('pk')
        obj = Pet.objects.get(id=petId)
        if obj is not None:
            if self.request.user.is_authenticated:
                for u in obj.users.all():
                    if u.id == self.request.user.id and u.user_type == 'S':
                        initial = super(PetImageCreate, self).get_initial(**kwargs)
                        return initial
                raise Http404
            else:
                raise Http404

    def form_valid(self, form):
        petId = self.kwargs.get('pk')
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

#############################################################################
# Edit Pet Functions:
# If user is authenticated and pet belongs to user, allows update to existing
# pet.  If user is not logged in, login page displays
# if user does not own pet, 404 displays
#############################################################################
class PetEdit(generic.UpdateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'status', 'description']
    template_name_suffix = '_update_form'

    #https://stackoverflow.com/questions/44935522/how-to-use-login-reuqired-on-update-create-delete-views-in-django
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PetEdit, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(PetEdit, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            for u in obj.users.all():
                if u.id == self.request.user.id and u.user_type == 'S':
                    return obj
            raise Http404
        else:
            raise Http404

#############################################################################
# Delete Pet
# brings up a confirmation screen. If confirm button is clicked,
# pet is removed from database.
#############################################################################
class PetDelete(generic.DeleteView):
    model = Pet
    success_url = reverse_lazy('pet:index')

    def get_object(self, *args, **kwargs):
        obj = super(PetDelete, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            for u in obj.users.all():
                if u.id == self.request.user.id and u.user_type == 'S':
                    return obj
            raise Http404
        else:
            raise Http404

#############################################################################
# Add/Remove Pet to Favorites
# Will add or remove pet from a user's (Pet Parent) favorites list
# Page will reload but not redirect so that this can be used on
# any screen with pet cards
#############################################################################
def addPetFavorite(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'P':
            petId = pk
            pet = Pet.objects.get(id=petId)
            if pet is not None:
                pet.users.add(request.user.id)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                raise Http404

def removePetFavorite(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'P':
            petId = pk
            pet = Pet.objects.get(id=petId)
            if pet is not None:
                pet.users.remove(request.user.id)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                raise Http404