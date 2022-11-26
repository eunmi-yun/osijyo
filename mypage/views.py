from django.shortcuts import render
from django.http import HttpResponse


def mypage(request):
    return render(request, 'mypage/mypage.html')