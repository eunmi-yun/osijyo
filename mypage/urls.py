from django.urls import path
from . import views

app_name = 'myPage'

urlpatterns = [
    path('', views.myPage),
]