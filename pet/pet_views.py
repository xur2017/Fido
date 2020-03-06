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

from django.contrib import messages
from PIL import Image
import time
from django.template import loader
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Pet, Picture, Status
from .filters import PetFilter
from . import feeds
from .forms import SendEmailForm
from django.conf import settings

# Create your views here.
def index(request):
    #https://docs.djangoproject.com/en/3.0/intro/tutorial03/
    status_list = Status.objects.order_by('-created_at')[:5]
    template = loader.get_template('pet/index.html')
    context = {
        'status_list': status_list,
    }
    return HttpResponse(template.render(context, request))

def emailView(request):
    if request.method == 'GET':
        msg = ''
        email_list = ''
        form = SendEmailForm()
    else:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            pet_id = form.cleaned_data['pet_id']
            message = form.cleaned_data['message']
            pet1 = Pet.objects.get(pk=pet_id)
            users1 = pet1.users.filter(user_type__exact='P')
            to_emails = list()
            for x in users1:
                to_emails.append(x.email)
            msg = 'message is already sent to'
            email_list = ','.join(to_emails)
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, to_emails)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    context = {'form': form, 'msg': msg, 'email_list': email_list}
    return render(request, "pet/email.html", context)

#https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
def sendEmail(statusId):
    subject = '''Team Fido: You've Got a Notification'''
    #pet_id = form.cleaned_data['pet_id']
    message = 'Test Message'
    pet1 = getattr(Status.objects.get(id=statusId), 'pet')
    prof = pet1.getprofile().photo
    stat_msg = getattr(Status.objects.get(id=statusId), 'status')
    #print(pet1)
    #pet1 = Pet.objects.get(pk=petId)
    #print(pet1)
    #pet_list = Pet.objects.filter(pk=petId)
    context ={
        'name': pet1.name,
        'profile': prof,
        'status': stat_msg,
        'MEDIA_URL':settings.MEDIA_URL,
        'MEDIA_ROOT':settings.MEDIA_ROOT,  
    }
    msg_html = render_to_string('user/email_notification.html', context)
    message =  strip_tags(msg_html)
    users1 = pet1.users.filter(user_type__exact='P')
    to_emails = list()
    for x in users1:
        if x.notify != 'N':
            to_emails.append(x.email)
    msg = 'email is already sent to'
    email_from = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, email_from, to_emails, html_message=msg_html)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

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
        context['status'] = Status.objects.filter(pet_id=petId).order_by('-created_at')
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
        context['status'] = Status.objects.filter(pet_id=petId).order_by('-created_at')
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

#View to allow rotation
class PetPicView(generic.DetailView):
    model = Picture

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        pic = Picture.objects.get(id=kwargs['pk'])
        if pic is not None:
            pet = Pet.objects.get(id=pic.pet.id)
            if pet is not None:
                if isShelterOwner(self.request, pet.id):
                    return super(PetPicView, self).dispatch(*args, **kwargs)
        raise Http404

#CreateView for Pet Images
class PetImageCreate(CreateView):
    model = Picture
    fields = ['description', 'photo','profile']

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

#UpdateView for Pet Images
class PetImageEdit(generic.UpdateView):
    model = Picture
    fields = ['description', 'photo']
    template_name_suffix = '_update_form'

    #https://stackoverflow.com/questions/44935522/how-to-use-login-reuqired-on-update-create-delete-views-in-django
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PetImageEdit, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(PetImageEdit, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            pet = Pet.objects.get(id=obj.pet.id)
            for u in pet.users.all():
                if u.id == self.request.user.id and u.user_type == 'S':
                    return obj
            raise Http404
        else:
            raise Http404

    def get_success_url(self, *args, **kwargs):
        obj = Picture.objects.get(id=self.kwargs['pk'])
        if obj.photo.name is not None and obj.photo.name is not "":
            return reverse('pet:viewpic', args=(obj.id,))
        else:
            return reverse('pet:pet_profile', args=(obj.pet.id,))

#http://garmoncheg.blogspot.com/2011/06/django-rotate-image-with-pil-usage.html
#Rotations
def rotate_left(request, pk):
    try:
        obj = Picture.objects.get(id=pk)
        pic = Image.open(obj.photo.file.name)
        pic_rotate = pic.rotate(90, expand=True)
        pic_rotate.save(obj.photo.file.name, overwrite=True)
        obj.photo = obj.photo.file.name
        obj.save()
        pic.close()
        pic_rotate.close()

        #added because page refresh was happening too quickly to see change
        time.sleep(1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except IOError:
        HttpResponse("cannot edit ", obj.photo.file.name)


def rotate_right(request, pk):
    try:
        obj = Picture.objects.get(id=pk)
        pic = Image.open(obj.photo.file.name)
        pic_rotate = pic.rotate(-90, expand=True)
        pic_rotate.save(obj.photo.file.name, overwrite=True)
        obj.photo = obj.photo.file.name
        obj.save()
        pic.close()
        pic_rotate.close()

        #added because page refresh was happening too quickly to see change
        time.sleep(1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except IOError:
        HttpResponse("cannot edit ", obj.photo.file.name)

class PetImageDelete(generic.DeleteView):
    model = Picture
    success_url = reverse_lazy('pet:index')

    def get_object(self, *args, **kwargs):
        obj = super(PetImageDelete, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            pet = Pet.objects.get(id=obj.pet.id)
            for u in pet.users.all():
                if u.id == self.request.user.id and u.user_type == 'S':
                    return obj
            raise Http404
        else:
            raise Http404

#############################################################################
# Create Pet Functions:
# createPet calls PetCreate to use CreateView
#############################################################################

#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'description']

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
                messages.add_message(request,messages.WARNING,
                    'You must be a Shelter to create a pet!',fail_silently=True)
                return HttpResponseRedirect('/')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

#############################################################################
# Pet Status Functions:
#############################################################################
class PetStatusCreate(CreateView):
    model = Status
    fields = ['status']

    def get_initial(self, queryset=None, *args, **kwargs):
        petId = self.kwargs.get('pk')
        obj = Pet.objects.get(id=petId)
        if obj is not None:
            if self.request.user.is_authenticated:
                for u in obj.users.all():
                    if u.id == self.request.user.id and u.user_type == 'S':
                        initial = super(PetStatusCreate, self).get_initial(**kwargs)
                        return initial
                raise Http404
            else:
                raise Http404

    def form_valid(self, form):
        petId = self.kwargs.get('pk')
        pet = Pet(id=petId)
        form.instance.pet = pet
        return super(PetStatusCreate, self).form_valid(form)

    def get_success_url(self):
        #Send email to pet parent's that have favorited
        petId = self.kwargs.get('pk')
        statusId = self.object.id
        sendEmail(statusId)
        return "/pet_profile/%i" % petId


class PetStatusListView(ListView):
    model = Status
    ordering = ['-created_at']
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#############################################################################
# Edit Pet Functions:
# If user is authenticated and pet belongs to user, allows update to existing
# pet.  If user is not logged in, login page displays
# if user does not own pet, 404 displays
#############################################################################
class PetEdit(generic.UpdateView):
    model = Pet
    fields = ['name', 'age', 'sex', 'pet_type', 'breed',
              'availability', 'disposition', 'description']
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

#############################################################################
# Helpers
#############################################################################
def isShelterOwner(request, petId):
    if request.user.is_authenticated:
        if request.user.user_type == 'S':
            pet = Pet.objects.get(id=petId)
            if pet is not None:
                for u in pet.users.all():
                    if u.id == request.user.id:
                        return True
    return False