
from django.contrib import admin
from django.urls import path
from .views import Inicio, SobreView

urlpatterns = [
    path("", Inicio.as_view(), name= "Inicio"),
    path('sobre-o-site/', SobreView.as_view(), name = "sobre"),
]
