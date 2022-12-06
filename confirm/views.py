from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from django.conf import settings
from django.contrib import messages

def confirm(request):
    return render(request,'confirm/confirm.html')

def upload_get(request):
    return render(request, 'confirm/upload.html')    

def imageCreate(request):
    if  'img_upload' in request.FILES:
        myfile = request.FILES['img_upload']
        fs = FileSystemStorage()
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)
        
        modelPath = os.path.join(settings.BASE_DIR, 'saved_model\\tomato_DenseNet201.h5')
        tomato_model = tf.keras.models.load_model(modelPath) 

        image = Image.open('media/'+myfile.name)
        resized_image = image.resize((224,224))
        image_arr = np.array(resized_image)

        # image_arr = np.array(image)
        predictions = tomato_model.predict(image_arr.reshape(1,224,224,3))
        print(predictions)
        # 예측값이 가장 높은 질병의 인덱스를 찾아옴
        idx = predictions[0].argmax()

        # 인덱스 번호를 질병명으로 바꿈.
        lables = ['세균점무늬병','겹무늬병','정상','잎마름역병','잎곰팡이병','흰무늬병','황화 잎말림 바이러스']
        result = lables[idx]
        url_lables=['https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00004333&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode=',
        'https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00001532&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode=',
        '','https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00001550&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode=',
        'https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00001533&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode=',
        'https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00001554&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode=',
        'https://ncpms.rda.go.kr/npms/ImageSearchInfoR4.np?detailKey=D00004252&moveKey=&queryFlag=V&upperNm=%EC%B1%84%EC%86%8C&kncrCode=VC010803&kncrNm=%ED%86%A0%EB%A7%88%ED%86%A0&nextAction=%2Fnpms%2FImageSearchDtlR4.np&finalAction=&flagCode=S&sPriyClCode='
        ]
        url_result=url_lables[idx]

        return render(request, 'confirm/result.html', {'result':result,'url_result':url_result})

    else:
        messages.warning(request, messages.warning, '이미지를 선택해 주세요!')
        return render(request,'confirm/confirm.html')

