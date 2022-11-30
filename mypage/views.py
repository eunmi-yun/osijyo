from django.shortcuts import render
from django.http import HttpResponse


def myPage(request):
    return render(request, 'myPage/myPage.html')