from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Animal(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Breed(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.animal.name}'


class Siting(BaseModel):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.breed.name} - {self.breed.animal.name} - {self.date}'