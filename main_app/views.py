# Add the 2 lines below
import uuid, boto3, os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bird, Toy, Feeding, Photo  # and import the Photo Model
from .forms import FeedingForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def birds_index(request):
    birds = Bird.objects.all()
    return render(request, 'birds/index.html', {
        'birds': birds
    })

def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  feeding_form=FeedingForm
  id_list = bird.toys.all().values_list('id')
  # Query for the toys that the bird doesn't have
  # by using the exclude() method vs. the filter() method
  toys_bird_doesnt_have = Toy.objects.exclude(id__in=id_list)
  # instantiate FeedingForm to be rendered in detail.html
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', {
    'bird': bird, 'feeding_form': feeding_form,
    'toys': toys_bird_doesnt_have
  })

def add_photo(request, bird_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to bird_id or bird (if you have a bird object)
            Photo.objects.create(url=url, bird_id=bird_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', bird_id=bird_id)

def add_feeding(request, bird_id):
   form = FeedingForm(request.POST)

   if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
    return redirect('detail', bird_id=bird_id)

def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  # Get the toys the bird doesn't have...
  # First, create a list of the toy ids that the bird DOES have
  id_list = bird.toys.all().values_list('id')
  # Now we can query for toys whose ids are not in the list using exclude
  toys_bird_doesnt_have = Toy.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', {
    'bird': bird, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_bird_doesnt_have
  })

class BirdCreate(CreateView):
  model = Bird
  fields = ['name', 'species', 'scientific_name', 'description', 'age']

class BirdUpdate(UpdateView):
   model=Bird
   fields = ['name', 'species', 'scientific_name', 'description', 'age']

class BirdDelete(DeleteView):
   model= Bird
   success_url = "/birds"

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys'

def assoc_toy(request, bird_id, toy_id):
  Bird.objects.get(id=bird_id).toys.add(toy_id)
  return redirect('detail', bird_id=bird_id)

def unassoc_toy(request, bird_id, toy_id):
  Bird.objects.get(id=bird_id).toys.remove(toy_id)
  return redirect('detail', bird_id=bird_id)