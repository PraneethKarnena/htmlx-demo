from django.urls import path

from siting.views import AnimalView


urlpatterns = [
    path('animals/', AnimalView.as_view(), name='animals_list'),
]