from django.shortcuts import render
from django.http import HttpResponse


def info(request):
    return render(request, 'info/info.html')