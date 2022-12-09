from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import history
from .forms  import StatusForm


def log(request):
    historys = history.objects.select_related('user_id','status_code','disease_code').order_by('history_id')
    return render(request, 'log/log.html',{"historys":historys})




def save(request) :
    if request.method == "POST":
            historys = history()
            historys.history_id = request.POST['history_id']
            historys.status_code = request.POST['tomatoSet']
            historys.save()
            return redirect('save')
    else:
        form = StatusForm
        context = {'form': form}
    return render(request, 'history/history.html',context)
