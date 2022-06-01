from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from siting.models import Animal, Breed, Siting


class HomeView(View):
    http_method_names = ['get']

    def get(self, request):
        return render(request, 'siting/home.html')


class AnimalView(View):
    http_method_names = ['get']

    def get(self, request):
        return JsonResponse({'success': True, 'data': list(Animal.objects.values('name', 'id'))})


class BreedView(View):
    http_method_names = ['get']

    def get(self, request, animal_id):
        return JsonResponse({'success': True, 'data': list(Breed.objects.filter(animal_id=animal_id).values('name', 'id'))})


@method_decorator(csrf_exempt, name='dispatch')
class SitingView(View):
    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        return JsonResponse({'success': True, 'data': list(Siting.objects.values('breed__name', 'id', 'date', 'breed__animal__name'))})


    def post(self, request):
        try:
            breed_id = request.POST.get('breed_id', None)
            date = request.POST.get('date', None)

            if None in (breed_id, date):
                raise Exception('breed_id and date are required!')

            _ = Siting.objects.create(breed_id=breed_id, date=date)
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'data': str(e)})


    def delete(self, request):
        try:
            siting_id = request.GET.get('siting_id', None)

            if siting_id is None:
                raise Exception('Siting ID is required!')

            _ = Siting.objects.get(id=siting_id).delete()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'data': str(e)})
