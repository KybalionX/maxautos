from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Coche(models.Model):
    placa = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(999)])
    precio = models.CharField(max_length=255, default=0)



class Imagen(models.Model):
    class Meta:
            verbose_name_plural = 'Imagenes'

    coche = models.ForeignKey('Coche', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="media", null=False, blank=False)

