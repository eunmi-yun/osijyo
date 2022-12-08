from django.urls import path
from . import views

app_name = 'confirm'

urlpatterns = [
    path('', views.confirm),
    path('imageCreate', views.imageCreate),
]