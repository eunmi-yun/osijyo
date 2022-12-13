from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('',views.info),
    path('loadChart',views.chart_allDisease),
]