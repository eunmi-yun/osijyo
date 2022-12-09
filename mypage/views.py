from django.shortcuts import render
from django.http import HttpResponse
from .models import history


def myPage(request):
    historys = history.objects.select_related('user_id','status_code','disease_code').order_by('history_id')
    return render(request, 'myPage/myPage.html',{"historys":historys})