from django.urls import path
from .views import *


urlpatterns = [
    path('coches/', CochesView.as_view()),
    path('coches/<int:id>', CocheById.as_view()),
    path('coches/<str:search>', CocheBySearch.as_view())
]