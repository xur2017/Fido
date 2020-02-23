from django.urls import path, include

from . import pet_views, user_views
from . import feeds

app_name = 'pet'

urlpatterns = [
    path('', pet_views.index, name='index'),
    path('pet/', pet_views.createPet, name='createpet'),
    path('pet/all', pet_views.PetListView.as_view(), name='petall'),
    path('pet/<int:pk>/', pet_views.PetDetailView.as_view(), name='petdetail'),
    path('pet/<int:pk>/edit', pet_views.PetEdit.as_view(), name='editpet'),
    path('pet/<int:pk>/pic', pet_views.PetImageCreate.as_view(), name='petpic'),
    path('pet/<int:pk>/delete', pet_views.PetDelete.as_view(), name='deletepet'),
    path('pic/<int:pk>/edit', pet_views.PetImageEdit.as_view(), name='editpic'),
    path('pic/<int:pk>', pet_views.PetPicView.as_view(), name='viewpic'),
    path('pic/<int:pk>/delete', pet_views.PetImageDelete.as_view(), name='deletepic'),
    path('pic/<int:pk>/rotateleft', pet_views.rotate_left, name='rotate_left'),
    path('pic/<int:pk>/rotateright', pet_views.rotate_right, name='rotate_right'),
    path('user/', user_views.createUser, name='createuser'),
    path('user/<int:pk>/', user_views.UserDetailView.as_view(), name='userdetail'),
    path('user/<int:pk>/pets', user_views.UserPetView.as_view(), name='userpetsview'),
    path('user/<int:pk>/edit', user_views.UserEdit.as_view(), name='edituser'),
    path('user/<int:pk>/delete', user_views.UserDelete.as_view(), name='deleteuser'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('pet_profile/<int:pk>/', pet_views.PetProfileView.as_view(), name='pet_profile'),
    path('user_profile/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile'),
    path('pet_filter', pet_views.search, name='pet_filter'),
    path('complete/', user_views.complete, name='complete'), #1
    path('pet/<int:pk>/addfavorite', pet_views.addPetFavorite, name='add_favorite'),
    path('pet/<int:pk>/removefavorite', pet_views.removePetFavorite, name='remove_favorite'),
    path('pet/about', pet_views.about, name='about'),
    path('pet/services', pet_views.services, name='services'),
    #path('pet/volunteer', pet_views.volunteer, name='volunteer'),
    
    path('feed/', feeds.LatestPetUpdates(), name='feed'),
    path('pet/favs', pet_views.FavListView.as_view(), name='petfavs'),
    path('email/', pet_views.emailView, name='email'),
    path('success/', pet_views.successView, name='success'),
]

