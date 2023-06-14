from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird

birds = [
    {'name': 'Polly', 'species': 'Scarlet Macaw', 'scientific_name': 'Ara Macao', 'description': "He's a walking stereotype. Loves crackers", 'age': '14'},
    {'name': 'Chester', 'species': 'Cockatiel', 'scientific_name': 'Nymphicus hollandicus', 'description': 'Loves headpats, and he can sing', 'age': '9'},
    {'name': 'Tiana', 'species': 'Sun Conure', 'scientific_name': 'Aratinga Solstitialis', 'description': 'Very energetic. He even dances', 'age': '22'},
]

# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def birds_index(request):
    return render(request, 'birds/index.html', {
        'birds': birds
    })

def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  return render(request, 'birds/detail.html', { 'bird': bird })

class BirdCreate(CreateView):
  model = Bird
  fields = '__all__'
  success_url = '/birds/{bird_id}'

class BirdUpdate(UpdateView):
   model=Bird
   fields=['species','scientific_name']

class BirdDelete(DeleteView):
   model= Bird
   success_url = "/birds"