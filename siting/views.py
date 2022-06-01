from django.http import JsonResponse
from django.views import View

from siting.models import Animal, Breed


class AnimalView(View):
    http_method_names = ['get']

    def get(self, request):
        return JsonResponse({'success': True, 'data': list(Animal.objects.values('name', 'id'))})


class BreedView(View):
    http_method_names = ['get']

    def get(self, request, animal_id):
        return JsonResponse({'success': True, 'data': list(Breed.objects.filter(animal_id=animal_id).values('name', 'id'))})