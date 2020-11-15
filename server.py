import re
from tensorflow import Graph, Session
import tensorflow as tf
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template
from flask import Flask, render_template, request,make_response
from flask_restful import Resource, Api, reqparse, abort
import json
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from werkzeug.utils import secure_filename
import os
from keras.models import load_model
from PIL import Image
import numpy as np
# Flask 인스턴스 정리
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)
api = Api(app)

#uploads_dir = os.path.join(app.instance_path, 'uploads')


#UPLOAD_FOLDER = 'C:\\Users\\cjb11\\PycharmProjects\\untitled2\\static\\img'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def facial_Emotion(filepath):

    imgName = (filepath)
    img = Image.open(imgName).convert('L')

    pixels = list(img.getdata())

    # 픽셀 값 reshape

    reshapeImgPixels = np.zeros((1, 48 * 48))

    for i in range(48 * 48):
        reshapeImgPixels[0, i] = int(pixels[i])

    img = reshapeImgPixels
    img = img / 255
    img = img.reshape((img.shape[0], 1, 48, 48))


    thread_graph = Graph()
    with thread_graph.as_default():
        thread_session=Session()
        with thread_session.as_default():
            model = load_model('./testModel/detectEmotionModel_epoch10.h5')
            global graph
            graph=tf.get_default_graph()

    with graph.as_default():
        with thread_session.as_default():
            global result
            result = model.predict(img)


    #result = model.predict(img)

    max = 0
    maxIdx = 0
    for i in range(0, 4):
        if result[0][i] > max:
            max = result[0][i]
            maxIdx = i

    if maxIdx == 0:
        emotion = 'Angry'
    elif maxIdx == 1:
        emotion = 'Happy'
    elif maxIdx == 2:
        emotion = 'Sad'
    elif maxIdx == 3:
        emotion = 'neutral'


    return emotion
    # 학습된 모델 load 후 예측


def Res_recommendation(feeling,location):

        options=webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        dv= webdriver.Chrome('C:\\Users\\cjb11\\Downloads\\chromedriver_win32\\chromedriver',chrome_options=options)
        dv.implicitly_wait(2)

        dv.get('https://map.naver.com/v5')

        #close_Button=dv.find_element_by_id('intro_popup_close')
        #close_Button.click()

        #container > div.router-output > shrinkable-layout > search-layout > search-box > div > div.search_box > button
        search_Bar=dv.find_element_by_class_name('span_search')
        search_Bar.click()

        dv.implicitly_wait(0.8)
        temp = dv.find_element_by_xpath(
            '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-box/div/div[1]/div/input')



        temp.send_keys(location)
        temp.send_keys(Keys.ENTER)

        btn  = dv.find_element_by_xpath(
            '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div/button')
        btn.click()

        #해피
        # if(feeling=='Happy'):
        #   feeling_Label = dv.find_element_by_xpath(
        #      '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[6]/label'
        # )
        #   feeling_Label2=dv.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[3]/label')
        #   feeling_Label.click()
        #   feeling_Label2.click()
        #   dv.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[4]/label').click()
        #   dv.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[3]/label').click()
        #   dv.find_element_by_xpath('//*[@id="container"]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[4]/div/button[2]').click()
        # dv.find_element_by_xpath(
        #     '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[4]/div/button[2]').click()
        #
        # dv.implicitly_wait(4)
        # asdf = []
        # for i in range(0, 4):
        #     asdf.append(dv.find_elements_by_class_name('search_title_text')[i].text)
        #
        # # res_list=soup.select('span.search_title_text')
        #
        # tmp = []
        #
        # for i in range(0, 4):
        #     name = re.compile('[가-힣0-9]+').findall(asdf[i])
        #     a = ' '.join(name)
        #
        #     tmp.append(a)
        #     return tmp
        #조용한 분위기 # 젊고 캐주얼한 날
        #elif(feeling=='Sad'):
         #   feeling_Label = dv.find_element_by_xpath(
          #      '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[2]/label'
           # )
            #feeling_Label2=dv.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[2]/ul/li[3]/label')
            #feeling_Label.click()
            #feeling_Label2.click()


            #dv.find_element_by_xpath('//*[@id="container"]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[4]/div/button[2]').click()
        # dv.find_element_by_xpath(
        #     '/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-tabs/div/div/div[2]/search-multi-filter/div[3]/div[4]/div/button[2]').click()
        #
        # dv.implicitly_wait(4)
        # asdf = []
        # for i in range(0, 4):
        #     asdf.append(dv.find_elements_by_class_name('search_title_text')[i].text)
        #
        # # res_list=soup.select('span.search_title_text')
        #
        # tmp = []
        #
        # for i in range(0, 4):
        #     name = re.compile('[가-힣0-9]+').findall(asdf[i])
        #     a = ' '.join(name)
        #
        #     tmp.append(a)
        #     return tmp

        req = dv.page_source
        soup=BeautifulSoup(req, 'html.parser')

        res_list=soup.select('span.search_title_text')

        tmp=[]
        recomen_list=[]
        recomen_list2=[]
        for res in res_list:
            name=re.compile('[가-힣]+').findall(res.text)
            a=' '.join(name)

            tmp.append(a)

        for i in range(0,len(tmp)):
            recomen_list.append(tmp[i])

        recomen_list2=random.sample(recomen_list,4)
        dv.quit()
        return recomen_list2

feeling= None
addr = None

@app.route('/address',methods=['POST'])
def Adr():
    global addr
    addr=""
    tmp=""
    tmp_str='동 맛집'
    tmp = request.get_json()
    tmp = tmp.split("동")
    tmp = ''.join(tmp[0])
    addr= tmp+tmp_str

    return addr

@app.route('/res', methods=['GET'])
def recommendation():
    result=""
    d=Res_recommendation(feeling,addr)
    result = {
        "res_list": ""
    }
    result.update(res_list=d)
    return jsonify(result)

@app.route('/image', methods=['POST'])
def upload():
   file = request.files['image']
   file.save('tmp.jpg')

   #file_path=uploads_dir+'\\'+file.filename
   global feeling
   feeling=""
   feeling = facial_Emotion("C:\\Users\\cjb11\\PycharmProjects\\untitled2\\tmp.jpg")
   return feeling



@app.route('/',methods=['GET'])
def startServer():
   return "hello "


@app.route('/result',methods=['GET'])
def getResult():
    temp=""
    temp = {
        "Emotion": ""
    }
    temp.update(Emotion=feeling)
    return jsonify(temp)


#host ="192.168.200.171",
if __name__ == '__main__':
    #Load_model()
    app.run( host ="192.168.221.100",debug=True)