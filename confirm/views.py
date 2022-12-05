from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import os
from django.conf import settings

def confirm(request):
    return render(request,'confirm/confirm.html')

# def imageCreate(request):
#     if request.method == 'POST':
#         myfile = request.FILES['img_upload']
#         fs = FileSystemStorage()
#         # FileSystemStorage.save(file_name, file_content)
#         filename = fs.save(myfile.name, myfile)
#         return render(request, 'confirm/confirm.html')
#     else:
#         return render(request, 'confirm/confirm.html')
def upload_get(request):
    return render(request, 'confirm/upload.html')    

def imageCreate(request):
    if request.method == 'POST':
        myfile = request.FILES['img_upload']
        fs = FileSystemStorage()
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)

        tomato_model =load_model(os.path.join(settings.BASE_DIR, 'saved_model/tomato_DenseNet201.h5')) 
        # tomato_model = tf.keras.models.load_model('saved_model/tomato_DenseNet201.h5')

        image = Image.open('media/'+myfile.name)
        resized_image = image.resize((160,160))
        image_arr = np.array(resized_image)

        # image_arr = np.array(image)
        predictions = tomato_model.predict(image_arr.reshape(1,160,160,3))
        print(predictions)
        # 예측값이 가장 높은 질병의 인덱스를 찾아옴
        idx = predictions[0].argmax()

        # 인덱스 번호를 질병명으로 바꿈.
        lables = ['세균점무늬병','겹무늬병','정상','잎곰팡이병','흰무늬병','황화 잎말림 바이러스']
        result = lables[idx]
        return render(request, 'confirm/result.html', {'result':result})
  

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