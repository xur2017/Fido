from django.urls import path

from . import views

app_name = 'pet'

urlpatterns = [
    path('', views.index, name='index'),
    path('createpet', views.createPet, name='createpet'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='petdetail'),
]