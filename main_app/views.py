# Add the 2 lines below
import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from .forms import FeedingForm
from .models import Bird, Feeding, Photo  # and import the Photo Model

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
  return render(request, 'birds/detail.html', { 'bird': bird })

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

class BirdCreate(CreateView):
  model = Bird
  fields = '__all__'

class BirdUpdate(UpdateView):
   model=Bird
   fields='__all__'

class BirdDelete(DeleteView):
   model= Bird
   success_url = "/birds"