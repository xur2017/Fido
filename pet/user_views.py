from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import CustomUser, Pet
from django.views.generic.edit import CreateView
from django.views import generic
from rest_framework import generics
from django.forms import ModelForm, forms
from django import forms
from django.contrib import messages

#############################################################################
# Create User Functions:
# createUser calls UserCreate to use ModelForm
# if ModelForm is valid, will create a new user
#############################################################################
#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class UserCreate(ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        template_name = 'user/user_form.html'
        model = CustomUser
        fields = ['user_type', 'first_name', 'last_name', 'email', 'username', 'password', 'password_confirm', 'phone_number',
                  'street_number', 'street_name', 'city', 'state', 'zip', 'profilePic']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
            'profilePic' : forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super(UserCreate, self).__init__(*args, **kwargs)
        self.fields['profilePic'].label = "Profile Picture"

    def clean(self):
        super(UserCreate, self).clean()
        error_message = ''
        field = ''
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            error_message = 'Passwords do not match.'
            field = 'password'
            self.add_error(field, error_message)
            raise forms.ValidationError(error_message)
        return self.cleaned_data

def createUser(request):
    test = request
    #if content_type = json, API request
    if request.content_type == 'application/json':
        return UserCreate.as_view()(request)
    else:
        #https://stackoverflow.com/questions/7576725/problem-using-djangos-user-authentication-model-uncomprehensible-error
        form=UserCreate(request.POST)
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
                return HttpResponseRedirect('%s' % user.id)
            else:
                return render(request, 'user/user_form.html', {'form': form})

#############################################################################
# View User Functions:
# View all details for a user
# profile returns separate htmls for each type of user
#############################################################################

#view user, this will send all user info for /user/<id> as context
class UserDetailView(generic.DetailView):
    model = CustomUser
    template_name = 'user/userdetail.html'

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