from django.urls import path, include

from . import pet_views, user_views

app_name = 'pet'

urlpatterns = [
    path('', pet_views.index, name='index'),
    path('pet/', pet_views.createPet, name='createpet'),
    path('pet/all', pet_views.PetListView.as_view(), name='petall'),
    path('pet/<int:pk>/', pet_views.PetDetailView.as_view(), name='petdetail'),
    path('pet/<int:pk>/edit', pet_views.PetEdit.as_view(), name='editpet'),
    path('pet/<int:pk>/pic', pet_views.PetImageCreate.as_view(), name='petpic'),
    path('user/', user_views.createUser, name='createuser'),
    path('user/<int:pk>/', user_views.UserDetailView.as_view(), name='userdetail'),
    path('user/<int:pk>/pets', user_views.UserDetailView.as_view(), name='userpetsview'),
    path('user/<int:pk>/edit', user_views.UserEdit.as_view(), name='edituser'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('pet_profile/<int:pk>/', pet_views.PetProfileView.as_view(), name='pet_profile'),
    path('user_profile/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile'),
    path('pet_filter', pet_views.search, name='pet_filter'),
    path('home/', user_views.home, name='home'), #1
    ]
#1. https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html

