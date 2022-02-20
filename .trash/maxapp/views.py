from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django_mysql.models import *
from .models import Coche
from operator import itemgetter
from django.db.models import Q
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from difflib import SequenceMatcher as SM


"""
Función que toma todas las imagenes de un vehiculo separadas por ',' y las convierte en un arreglo. Ej:

"image1.jpg,image2.jpg,image3.jpg" = ["ruta/image1.jpg", "ruta/image.jpg", "ruta.image3.jpg"]

En caso de que el parametro sea None, se deja la ruta de una imagen por defecto
"""
def SplitImage(images):
    if images is None:
        images = "media/no_resource.png"
    return map(lambda e : "https://maxautos.pythonanywhere.com/media/"+e, images.split(','))


class CochesView(APIView):

    def get(self, request, format=None):
        coches = Coche.objects.annotate(image_list=GroupConcat('imagen__imagen')).values('id', 'marca', 'modelo', 'cantidad', 'precio', 'placa', 'image_list')

        data = []
        for c in coches:
            coche = {}
            coche['id'], coche['marca'], coche['modelo'], coche['precio'], coche['placa'] = itemgetter('id', 'marca', 'modelo', 'precio', 'placa')(c)
            #coche['imagenes'] = map(lambda e : "https://maxautos.pythonanywhere.com/media/"+e, c['image_list'].split(','))
            coche['imagenes'] = SplitImage(c['image_list'])
            data.append(coche)

        return Response(data)

class CocheById(APIView):

    def get(self, request, id=0):
        cid = id
        try:
            coche = Coche.objects.annotate(image_list=GroupConcat('imagen__imagen')).values('id', 'marca', 'modelo', 'cantidad', 'precio', 'placa', 'image_list').get(id=cid)
            coche['imagenes'] =  SplitImage(coche['image_list'])
        except Coche.DoesNotExist:
            coche = []
        return Response(coche)


class CocheBySearch(APIView):

    def get(self, request, search):

        coches = Coche.objects.annotate(image_list=GroupConcat('imagen__imagen'), nombre=Concat('marca', V(' '), 'modelo')).values('id', 'marca', 'modelo', 'cantidad', 'precio', 'placa', 'image_list', 'nombre').filter(Q(modelo__icontains = search) | Q(marca__icontains = search) | Q(nombre__icontains = search))

        data = []

        if len(coches) == 0:
            for c in Coche.objects.annotate(image_list=GroupConcat('imagen__imagen'), nombre=Concat('marca', V(' '), 'modelo')).all():
                if SM(None, c.marca.lower(), search.lower()).ratio() >= 0.5 or SM(None, c.modelo.lower(), search.lower()).ratio() >= 0.5:
                    coche = {}
                    coche['id'] = c.id
                    coche['marca'] = c.marca
                    coche['modelo'] = c.modelo
                    coche['precio'] = c.precio
                    coche['placa'] = c.placa
                    coche['imagenes'] = SplitImage(c.image_list)
                    #coche['ratioMarca'] = SM(None, c.marca, search).ratio()
                    #coche['ratioModelo'] = SM(None, c.modelo, search).ratio()
                    data.append(coche)
                else:
                    continue
        else:
            for c in coches:
                coche = {}
                coche['id'], coche['marca'], coche['modelo'], coche['precio'], coche['placa'] = itemgetter('id', 'marca', 'modelo', 'precio', 'placa')(c)
                coche['imagenes'] = SplitImage(c['image_list'])
                data.append(coche)

        return Response(data)
