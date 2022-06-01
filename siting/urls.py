from django.urls import path

from siting.views import AnimalView, BreedView, SitingView


urlpatterns = [
    path('animals/', AnimalView.as_view(), name='animals_list'),
    path('breeds/<uuid:animal_id>/', BreedView.as_view(), name='breeds_list'),
    path('sitings/', SitingView.as_view(), name='sitings_list'),
]