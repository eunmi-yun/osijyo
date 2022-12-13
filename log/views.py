from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import history
from django.core.paginator import Paginator





def log(request):
    historys = history.objects.order_by('-history_id')
    paginator = Paginator(historys, 20)
    page = int(request.GET.get('page', 1))
    history_list = paginator.get_page(page)
    return render(request, 'log/log.html',{'title':'HISTORY PAGE','history_list':history_list})



