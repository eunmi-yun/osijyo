# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import connection
import matplotlib.pyplot as plt
from os.path import isfile
from django.db import connection
import numpy as np
import platform
import log.models
from collections import defaultdict
import os
import seaborn as sns

def info(request):
    clearChart('static/info/')
    return render(request, 'info/info.html')

#한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus']=False
if platform.system()=='Darwin':
    rc('font',family='AppleGothic')
elif platform.system()=='Windows':
    path='C:/Windows/Fonts/malgun.ttf'
    font_name=font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)
else:
    print('Unknown system...')



def saveDataToGraph(_dict, _root):
    nameList = _dict.keys()
    monthList = []
    yList = np.arange(12)

    for i in range(12):
        monthList.append(i + 1)

    for name in nameList:
        plt.figure(figsize=(6,4))
        plt.title('<'+name +'> 보고 건수',fontsize=15)
        plt.xlabel('Month')         
        plt.ylabel('Disease count')
        plt.bar(yList, _dict[name][1:],color="pink")
        plt.xticks(yList, monthList)
        name = name.replace(' ', '_')
        filePath = _root + name + '.png'
        plt.ylim(0,150)
        plt.savefig(filePath)
        plt.clf()


    #누적 막대그래프        
    colors=sns.color_palette('Set3',len(nameList))
    i = 0
   
    for name in nameList:
        plt.bar(yList, _dict[name][1:],label=name, color=colors[i])
        print(name)
        print(_dict[name][1:])
        i += 1
    
    #lists = []
    #for name in nameList
    #   lists.append(_Dic[name][1:])

    # plt.bar(nameList, lists, color=colors)
    
    plt.xticks(yList, monthList)
    plt.title("총 질병 보고 건수",fontsize=15)
    plt.xlabel('Month')         
    plt.ylabel('Disease count')
    plt.spring()    
    plt.ylim(0,300)    
    plt.legend()
    plt.savefig(_root + 'total.png')
    plt.clf()




def clearChart(_root):
    nameList = ['겹무늬병', '세균점무늬병', '잎곰팡이병', '잎마름역병', '황화_잎말림_바이러스', '흰무늬병', 'total']
    for name in nameList:
        filePath = _root + name + '.png'
        if os.path.exists(filePath) == True:
            os.remove(filePath)



def chart_allDisease(request):
    selectYear=request.POST.get('year')
    cursor = connection.cursor() 
   
    sql = 'Select YEAR(reg_date), MONTH(reg_date), disease_name from history where YEAR(reg_date)='+selectYear
    cursor.execute(sql)
    dataList=cursor.fetchall()

    statisticsList = defaultdict(list)

    for year, month, name in dataList:
        if len(statisticsList[name]) == 0:
            tmpList = [0 for i in range(13)]
            statisticsList[name] = tmpList
        statisticsList[name][month] += 1

    saveDataToGraph(statisticsList, 'static/info/')

    return render(request, 'info/info.html')
    

