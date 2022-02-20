from django.urls import path
from .views import *
from django.conf.urls.static import static



urlpatterns = [
    path('coches/', CochesView.as_view()),
    path('coches/<int:id>', CocheById.as_view()),
    path('coches/<str:search>', CocheBySearch.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)