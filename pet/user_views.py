from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import CustomUser, Pet
from django.views import generic

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import CreateUserForm

#############################################################################
# Create User Functions:
# createUser calls CreateUserForm to use ModelForm
# if ModelForm is valid, will create a new user
#############################################################################
#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
def createUser(request):
    test = request
    #if content_type = json, API request
    if request.content_type == 'application/json':
        return CreateUserForm.as_view()(request)
    else:
        #https://stackoverflow.com/questions/7576725/problem-using-djangos-user-authentication-model-uncomprehensible-error
        form=CreateUserForm(request.POST)
        if request.method == 'GET':
            return  render(request, 'user/user_form.html', { 'form': form })
        elif request.method == 'POST':
            if form.is_valid():
                user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
                                                      password=form.cleaned_data['password'],
                                                      email=form.cleaned_data['email'])
                user.set_password(form.cleaned_data['password'])
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.street_number = form.cleaned_data['street_number']
                user.street_name = form.cleaned_data['street_name']
                user.city = form.cleaned_data['city']
                user.state = form.cleaned_data['state']
                user.zip = form.cleaned_data['zip']
                user.user_type = form.cleaned_data['user_type']
                user.save()
                return render(request, 'user/user_create_success.html', {'username': user.username })
            else:
                return render(request, 'user/user_form.html', {'form': form})

#############################################################################
# View User Functions:
# View all details for a user
# profile returns separate htmls for each type of user
#############################################################################

#view user, this will send all user info for /user/<id> as context
#for user's view only, not general public
class UserDetailView(generic.DetailView):
    model = CustomUser
    template_name = 'user/userdetail.html'

    def get_object(self, queryset=None, *args, **kwargs):
        if self.request.user.is_authenticated:
            obj = super(UserDetailView, self).get_object(*args, **kwargs)
            if obj.id == self.request.user.id:
                return obj
            else:
                raise Http404
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userId = self.kwargs.get('pk')
        context['pets'] = Pet.objects.filter(users=userId)
        return context

def profile(request):
    #sends list of favorite pets AND/OR shelter's pets
    userId = request.user.id
    context = { 'request': request }
    context['pets'] = Pet.objects.filter(users=userId)
    if request.user.user_type == 'S':
        return render(request, 'user/profileShelter.html', context)
    elif request.user.user_type == 'P':
        return render(request, 'user/profileParent.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

#general Public view
class UserProfileView(generic.DetailView):
    context_object_name = 'user'
    model = CustomUser
    template_name = 'user/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userId = self.kwargs.get('pk')
        context['pets'] = Pet.objects.filter(users=userId)
        return context

class UserPetView(generic.DetailView):
    model = CustomUser
    template_name = 'user/userPets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userId = self.kwargs.get('pk')
        context['pets'] = Pet.objects.filter(users=userId)
        return context

#############################################################################
# Edit User Functions:
# Allows user to update profile if authenticated and is user
#############################################################################
class UserEdit(generic.UpdateView):
    model = CustomUser
    fields = [ 'first_name', 'last_name', 'email', 'phone_number',
                      'street_number', 'street_name', 'city', 'state', 'zip', 'profilePic']
    template_name= 'user/user_update_form.html'
    widgets = {
        'password': forms.PasswordInput(),
        'email': forms.EmailInput(),
        'profilePic' : forms.ImageField()
    }


    def get_object(self, *args, **kwargs):
        obj = super(UserEdit, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            if obj.id == self.request.user.id:
                return obj
            raise Http404
        else:
            raise Http404

#############################################################################
# Delete User Functions:
# Allows user to delete profile if authenticated and is user
#############################################################################
class UserDelete(generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy('pet:index')
    template_name = 'user/customuser_confirm_delete.html'

    def get_object(self, *args, **kwargs):
        obj = super(UserDelete, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            if obj.id == self.request.user.id:
                #remove any associated pets
                if obj.user_type == 'S':
                    petsList = Pet.objects.filter(users=obj.id)
                    for pet in petsList:
                        pet.delete()
                return obj
        raise Http404

#############################################################################
# Landing Page Function:
# Simple landing page for login completions
#############################################################################

#1. https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
#2. https://scotch.io/tutorials/django-authentication-with-facebook-instagram-and-linkedin
#3. https://medium.com/trabe/oauth-authentication-in-django-with-social-auth-c67a002479c1
@login_required
def complete(request):
    return render(request, 'registration/complete.html')
