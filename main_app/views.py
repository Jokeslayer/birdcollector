from django.shortcuts import render

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