from django.urls import path

from siting.views import AnimalView, BreedView, SitingView, HomeView, DateView


urlpatterns = [
    path('animals/', AnimalView.as_view(), name='animals_list'),
    path('breeds/', BreedView.as_view(), name='breeds_list'),
    path('sitings/', SitingView.as_view(), name='sitings_list'),
    path('dates/', DateView.as_view(), name='date_list'),
    path('', HomeView.as_view(), name='home'),
]