from django.shortcuts import render
from django.http import HttpResponse


def history(request):
    return render(request, 'history/history.html')