
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)

            # Define las dimensiones deseadas (ancho, alto)
            new_dimensions = (300, 200)

            # Escala la imagen
            img.thumbnail(new_dimensions)

            # Guarda la imagen escalada
            img.save(self.photo.path)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

