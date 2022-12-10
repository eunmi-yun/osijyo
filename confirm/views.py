from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os
from django.conf import settings
from django.contrib import messages
import cv2
import numpy as np
import tensorflow as tf
from log.models import history
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect
from log.views import log

def confirm(request):
    return render(request,'confirm/confirm.html')

def upload_get(request):
    return render(request, 'confirm/upload.html')   

def save(request):
    if request.method == 'POST':
        history_list = history()
        history_list.reg_date = datetime.now()
        history_list.disease_cure = request.POST['disease_cure']
        history_list.disease_name = request.POST['disease_name']
        history_list.save()
        return log(request)
    else :
        history_list = history.objects.all()
        return log(request)




def imageCreate(request):
    if  'img_upload' in request.FILES:
        myfile = request.FILES['img_upload']
        fs = FileSystemStorage()
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)

        if 'btn_yolo' in request.POST:
            weight_path = "saved_model/yolov3_final.weights"
            config_path = "saved_model/yolov3.cfg"

            cv_net_yolo = cv2.dnn.readNetFromDarknet(config_path, weight_path)

            layers_names = cv_net_yolo.getLayerNames()
            outlayer_names = [layers_names[i-1] for i in cv_net_yolo.getUnconnectedOutLayers()]
            # 1부터 시작해야 하는데, 인덱스 번호는 0부터 시작하기 때문에 1씩 빼준다.

            img = cv2.imread('media/'+myfile.name)

            # 해당 모델은 608 * 608 이미지를 받기 때문에, img 크기를 지정해준다.
            cv_net_yolo.setInput(cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(608, 608), swapRB=True, crop=False))

            cv_out = cv_net_yolo.forward(outlayer_names)
            # layer 이름을 넣어주면, 해당하는 output을 return한다.

            # 바운딩 박스 그리기 (output에서 bounding box 정보 추출)

            # 1/255.0 스케일링된 값을 추후 복원시킨다.
            rows = img.shape[0]
            cols = img.shape[1]

            conf_threshold = 0.3 # confidence score threshold

            class_ids = []
            confidences = []
            boxes = []

            for _, out in enumerate(cv_out):
                for _, detection in enumerate(out):
                    class_scores = detection[5:] # 인덱스 5 다음부터는 2개의 score 값
                    class_id = np.argmax(class_scores) # 2개 중 최대값이 있는 index 값
                    confidence = class_scores[class_id] # 최대값 score
                    
                    if confidence > conf_threshold:
                        # 바운딩 박스 중심 좌표와 박스 크기
                        # 0~1 사이로 리사이즈 되어있기 때문에, 입력이미지에 맞는 좌표계산을 위해 곱한다.
                        cx = int(detection[0] * cols)
                        cy = int(detection[1] * rows)
                        bw = int(detection[2] * cols)
                        bh = int(detection[3] * rows)
                        
                        # 바운딩 박스를 그리기 위해서 좌상단 점이 필요함
                        left = int(cx - bw / 2)
                        top = int(cy - bh /2)
                        
                        class_ids.append(class_id) # class id 값 담기
                        confidences.append(float(confidence)) # confidence score 담기
                        boxes.append([left, top, bw, bh]) # 바운딩 박스 정보 담기

                        
            labels_to_names_seq = {0:'disease sopt', 1:'disease area'}


            nms_threshold = 0.4 # nonmaxsuppression threshold

            # opencv 제공하는 nonmaxsuppression 함수를 통해 가장 확률 높은 바운딩 박스 추출
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

            draw_img = img.copy() # 그림 그리기 위한 도화지

            # 같은 라벨 별로 같은 컬러를 사용하기 위함, 사용할 때마다 랜덤하게 컬러 설정
            colors = np.random.uniform(0, 255, size=(len(labels_to_names_seq), 3))

            # 바운딩 박스가 없을 경우를 대비하여 1개 이상일 때만 실행하도록 한다.
            if len(idxs) > 0:
                for i in idxs:
                    box = boxes[i]
                    left = box[0]
                    top = box[1]
                    width = box[2]
                    height = box[3]
                    
                    caption = f"{labels_to_names_seq[class_ids[i]]}: {confidences[i]:.2})"
                    label = colors[class_ids[i]]
                    cv2.rectangle(draw_img, (int(left), int(top), int(width), int(height)), color=label, thickness=2)
                    cv2.putText(draw_img, caption, (int(left), int(top-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, label, 2, cv2.LINE_AA)

            # cv2.imwrite('media/yolo/'+myfile.name, draw_img)
            cv2.imwrite('media/yolo/result_img.jpg', draw_img)

            if boxes == []:
                result = '건강합니다'
            else:
                result = '질병에 걸렸습니다.'   


            return render(request, 'confirm/result_yolo.html', {'result':result})
        
        else:
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
            result2_lables = ['하우스 내부를 청결하게 관리하고 다습하지 않도록 통풍과 환기를 잘 시킨다.','온실재배 시 내부가 다습하지 않도록 환기를 한다','정상','항상 포장을 청결히 하고 병든 잎이나 줄기는 조기에 제거하여 불에 태우거나 땅속 깊이 묻는다.','90%이상의 상대습도가 유지되지 않도록 해야 하고 통풍이 잘되게 하고 밀식하지 않는다.','종자를 선별하고, 소독하여 파종 해야 하며 재배 시 균형시비를 하고 병든 잎은 조기에 제거한다.','담배가루이 약제를 처리하여 박멸']
            result2= result2_lables[idx]
            return render(request, 'confirm/result_cnn.html', {'result':result,'url_result':url_result,'result2':result2})

    else:
        messages.warning(request, messages.warning, '이미지를 선택해 주세요!')
        return render(request,'confirm/confirm.html')



