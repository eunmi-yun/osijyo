from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def confirm(request):
    return render(request,'confirm/confirm.html')

def imageCreate(request):
    if request.method == 'POST':
        myfile = request.FILES['img_upload']
        fs = FileSystemStorage()
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)
        return render(request, 'confirm/confirm.html')
    else:
        return render(request, 'confirm/confirm.html')
    

 