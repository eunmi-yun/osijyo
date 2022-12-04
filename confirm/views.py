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
    


# def imageCreate(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES) # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
#         if form.is_valid():
#             image = form.save(commit=False)
#             image.author = request.user
#             image.save()
#             return redirect('confirm/confirm.html')
#     else:
#         form = ImageForm() # request.method 가 'GET'인 경우
#     context = {'form':form}
#     return render(request, 'confirm/confirm.html', context)    