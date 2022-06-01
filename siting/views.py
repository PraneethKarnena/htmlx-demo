from django.http import JsonResponse
from django.views import View

from siting.models import Animal, Breed


class AnimalView(View):

    def get(self, request):
        return JsonResponse({'success': True, 'data': list(Animal.objects.values('name', 'id'))})