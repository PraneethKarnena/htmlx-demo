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
        animals = Animal.objects.all()
        animals_list = '<option value=""></option>'

        for animal in animals:
            animals_list += f'<option value="{animal.id}">{animal.name}</option>'

        response = f'''<div class="form-group">
                            <label for="animalInput">Animal</label>
                            <select class="form-control" id="animalInput" name="animal_id" hx-trigger="change" hx-post="/breeds/" hx-target="#breedsList" required>
                                {animals_list}
                            </select>
                        </div>
                            <div id="breedsList"></div>
                            <button type="submit" class="btn btn-primary mt-2" >Save</button>
                            <button type="button" class="btn btn-danger mt-2 ml-2" hx-trigger="click" hx-get="/breeds/" hx-target="#animalsList">Cancel</button>
                        '''
        return HttpResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class BreedView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        return HttpResponse('')

    def post(self, request):
        animal_id = request.POST.get('animal_id', None)

        if animal_id is None:
            return HttpResponse('Error: Animal ID is required')

        breeds_list = '<option value=""></option>'
        breeds = Breed.objects.filter(animal_id=animal_id)

        for breed in breeds:
            breeds_list += f'<option value="{breed.id}">{breed.name}</option>'

        response = f'''<div class="form-group">
                            <label for="breedInput">Breed</label>
                            <select class="form-control" id="breedInput" name="breed_id" hx-trigger="change" hx-get="/dates/" hx-target="#dateList" required>
                                {breeds_list}
                            </select>
                        </div>
                        <div id="dateList"></div>
                        '''
                        
        return HttpResponse(response)


class DateView(View):
    http_method_names = ['get']

    def get(self, request):
        response = f'''<div class="form-group">
                            <label for="dateInput">Date</label>
                            <input type="date" class="form-control" id="dateInput" name="date" required>
                        </div>
                        '''
        return HttpResponse(response)


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
            return HttpResponse('')

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
