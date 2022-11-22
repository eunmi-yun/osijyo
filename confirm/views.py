from django.shortcuts import render
from django.http import HttpResponse


def confirm(request):
    return render(request, 'confirm/confirm.html')