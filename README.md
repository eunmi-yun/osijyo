# 토마토 질병 분류 웹서비스

## 멀티캠퍼스 세번째 프로젝트 : osijyo (오시죠)

딥러닝 CNN, YOLO 모델을 이용한 토마토 질병 분류 서비스와 함께 질병 탐색 기록, 통계 그래프 등 부가 서비스를 제공하는 프로젝트
<br></br>
![간단 이미지 경로](https://user-images.githubusercontent.com/110808089/207804448-efd52709-e3db-416c-bbf6-f2d8c304305c.png)

#

## 1. 서비스 설명

- 사용자로부터 사진을 입력 받음
- 간편 확인(YOLO 모델) 또는 상세 확인(CNN 모델)을 거쳐 질병 결과 값 추출
- 질병에 따른 각각의 대처법 페이지 제공
- 질병 탐색 결과 DB 구축
- DB를 이용해서 통계 페이지, 히스토리 페이지 제공
  <br></br>
  ![순서도](https://user-images.githubusercontent.com/110808089/207804707-4822b0c3-7779-453b-ad19-44e960352a6f.png)

<br></br>

## 2. 웹 페이지 설명

![화면 설계도](https://user-images.githubusercontent.com/110808089/207804670-de21a62c-9596-43c9-90d4-f75d49aac127.png)

<br></br>

## 3. 개발 환경 및 사용 라이브러리

- Language : Python 3.8, HTML5, JavaScript, CSS
- Framework : Django
- DBMS : MySQL
- AI : CNN, YOLO, TensorFlow2

#

## 환경설정 (Anaconda)

- conda env create -f serverReal.yaml
- conda activate serverReal
