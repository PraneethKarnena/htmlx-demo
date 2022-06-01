from django.http import JsonResponse, HttpResponse
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

    def get_sitings(self):
        response = ''
        sitings = Siting.objects.all()
        for idx, siting in enumerate(sitings):
            response += f'''<tr>
                            <th scope="row">{idx+1}</th>
                            <td>{siting.breed.animal.name}</td>
                            <td>{siting.breed.name}</td>
                            <td>{siting.date}</td>
                            <td><button hx-trigger="click" hx-delete="/sitings/?siting_id={siting.id}" hx-target="#sitings_list" class="btn btn-sm btn-danger" type="button">DELETE</button></td>
                            </tr>'''
        
        return response

    def get(self, request):
        return HttpResponse(self.get_sitings())


    def post(self, request):
        try:
            breed_id = request.POST.get('breed_id', None)
            date = request.POST.get('date', None)

            if None in (breed_id, date):
                raise Exception('breed_id and date are required!')

            _ = Siting.objects.create(breed_id=breed_id, date=date)
            return HttpResponse(self.get_sitings())

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')


    def delete(self, request):
        try:
            siting_id = request.GET.get('siting_id', None)

            if siting_id is None:
                raise Exception('Siting ID is required!')

            _ = Siting.objects.get(id=siting_id).delete()

            return HttpResponse(self.get_sitings())

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
