from django.contrib import admin

# Register your models here

from .models import Bird, Feeding, Toy, Photo

admin.site.register(Bird)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)
