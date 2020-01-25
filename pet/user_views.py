from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import CustomUser
from django.views.generic.edit import CreateView
from django.views import generic
from rest_framework import generics
from django.forms import ModelForm

# Create your views here.
#view user, this will send all user info for /user/<id> as context
class UserDetailView(generic.DetailView):
    model = CustomUser
    template_name = 'user/userdetail.html'

#############################################################################
# Create User Functions:
# createUser calls UserCreate to use CreateView
#############################################################################
#https://riptutorial.com/django/example/3998/form-and-object-creation
#https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
class UserCreate(ModelForm):
    class Meta:
        template_name = 'user/user_form.html'
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone_number']

    #def form_valid(self, form):
    #    return super().form_valid(form)

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
                return HttpResponseRedirect('%s' % user.id)
            else:
                raise ValueError()

def profile(request):
    return render(request, 'user/profile.html')