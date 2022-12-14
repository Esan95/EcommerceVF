from django.db import models
from django.conf import settings
import os
from django.core.validators import FileExtensionValidator

class Persona(models.Model):
    rut = models.CharField(primary_key=True, max_length=13)
    nombre = models.CharField(max_length=20)
    correo_electronico = models.CharField(unique=True, max_length=40)
    direccion = models.CharField(max_length=50)
    contrasenna = models.CharField(max_length=15)
    telefono = models.CharField(max_length=15)
    perfil = models.CharField(max_length=15)


def marketplace_directory_path(instance, filename):
    banner_pic_name='products/{0}/{1}'.format(instance.name, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)
    return banner_pic_name


    
# Create your models here.
class Productos(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField()
    thumbnail = models.ImageField(blank=True, null=True, upload_to="productos")
    slug=models.SlugField(unique=True)
    content_file = models.FileField(blank=True, null=True)
    active = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

    def price_display(self):
        return "{0:.2f}".format(self.price / 100)


class productosComprados(models.Model):
    rut = models.ForeignKey(Persona,on_delete=models.CASCADE, related_name="products")
    email = models.EmailField()
    Productos = models.ForeignKey(Productos, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email