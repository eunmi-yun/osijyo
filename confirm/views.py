from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os
from django.conf import settings
from django.contrib import messages
import cv2
import numpy as np
import tensorflow as tf
from log.views import logView
from log.models import history
from datetime import datetime


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

                        
            labels_to_names_seq = {0:'disease spot', 1:'disease area'}


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
                    
                    caption = f"{labels_to_names_seq[class_ids[i]]}: {confidences[i]:.2}"
                    label = colors[class_ids[i]]
                    cv2.rectangle(draw_img, (int(left), int(top), int(width), int(height)), color=label, thickness=2)
                    cv2.putText(draw_img, caption, (int(left), int(top-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label, 2, cv2.LINE_AA)

            # cv2.imwrite('media/yolo/'+myfile.name, draw_img)
            cv2.imwrite('media/yolo/result_img.jpg', draw_img)

            if boxes == []:
                result = '건강합니다'
            else:
                result = '질병에 걸렸습니다.'   

            os.remove('media/'+ myfile.name)
            return render(request, 'confirm/result_yolo.html', {'result':result})
        
        else:
            #DB에 이미지 경로 저장
            savedHistory = history()
            savedHistory.reg_date = datetime.now()
            savedHistory.photo = myfile
            modelPath = os.path.join(settings.BASE_DIR, 'saved_model\\model_DN121_2.h5')
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

            result3_lables=['병 발생 초기에 잎에 담갈색∼암갈색을 띤 작은 반점이 수침상으로 형성된다.','잎, 줄기, 과실에 발생한다. 처음에 타원형의 갈색 반점으로 나타나고 진전되면 암갈색의 겹무늬 반점으로 확대된다.','','잎, 과실, 줄기 등에서 발생한다.  병든 잎은 연한 녹색이나 갈색으로 썩고, 과실의 병든 부위는 흑갈색으로 썩는다. 비교적 단단하며 과실전체가 심하게 오그라들기도 한다','잎에 발생한다. 처음에는 잎의 표면에 흰색 또는 담회색의 반점으로 나타나고 진전되면 황갈색 병반으로 확대된다','잎, 잎자루, 줄기, 가지, 과경에 발생한다.감염 부위에는 갈색 내지 암갈색의 작은 반점이 형성되고, 진전되면 병반의 내부는 회색으로 변한다.','잎이 누렇게 오그라드는 잎말림 증상이 나타나고, 줄기는 위축돼 정상적인 생육이 되지 않는다. 또 꽃이 잘 피지 않고, 열매는 착색불량 증상을 보인다.']
            result3= result3_lables[idx]
            
            history_list = history()
            history_list.reg_date = datetime.now()
            history_list.disease_cure = result2
            history_list.disease_name = result
            history_list.photo = myfile
            historyResult = history_list.photo
            history_list.save()
            # os.remove('media/'+ myfile.name)
            print(historyResult)
            return render(request, 'confirm/result_cnn.html', {'result':result,'url_result':url_result,'result2':result2, 'historyResult':historyResult,'result3':result3})

    else:
        messages.warning(request, messages.warning, '이미지를 선택해 주세요!')
        return render(request,'confirm/confirm.html')