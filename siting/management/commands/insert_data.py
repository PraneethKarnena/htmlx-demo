import json
from unicodedata import name

from django.core.management.base import BaseCommand, CommandError
from siting.models import Animal, Breed

class Command(BaseCommand):
    help = 'Insert initial data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Inserting animals data...'))
        animals = None

        with open('animals.json', 'r') as animals_data:
            animals = json.loads(animals_data.read())

        for animal in animals:
            _, _ = Animal.objects.get_or_create(name=animal)

        self.stdout.write(self.style.SUCCESS('Inserted animals data successfully...'))

        self.stdout.write(self.style.WARNING('Inserting breeds data...'))
        breeds = None

        with open('breeds.json', 'r') as breeds_data:
            breeds = json.loads(breeds_data.read())

        for animal, breeds_list in breeds.items():
            animal = Animal.objects.get(name=animal)
            
            for breed in breeds_list:
                _, _ = Breed.objects.get_or_create(animal=animal, name=breed)

        self.stdout.write(self.style.SUCCESS('Inserted breeds data successfully...'))
