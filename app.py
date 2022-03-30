from dis import code_info
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import simplejson as json
# from bson import ObjectId
# from bson.objectid import ObjectId
from bson.json_util import dumps
import requests
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

client = MongoClient('mongodb://test:test@54.180.139.22', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmuckji  # 'dbmuckji'라는 이름의 db를 만들거나 사용합니다.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/addpage')
def addPage():
   return render_template('add.html')

@app.route('/api/addPhoto')
def addPhoto():
   return render_template('addPhoto.html')

@app.route('/api/add', methods=['POST'])
def addMenu():
    # 1. 클라이언트로부터 데이터를 받기
    food_receive = request.form['food_give']
    category_receive = request.form['category_give']
    shop_name_receive= request.form['shop_name_give']
    shop_address_receive= request.form['shop_address_give']
    
    # 3. dbmuckji DB로 보낼 데이터 정리
    food = {
            'food_name': food_receive, 
            'food_category': category_receive, 
            'shop_name': shop_name_receive,
            'shop_address': shop_address_receive,
            'shop_img': 0,
            'like':0,    # like를 0으로 세팅
            'hate':0,    # hate를 0으로 세팅
            'food_code':0, # food_code를 0으로 세팅
            'shop_url':0
            # 'shop_url':url_receive,
            }
    
    # 3. mongoDB에 데이터 넣기
    # insert_one()은 inserted_id 속성을 지닌 object 리턴
    x = db.shop.insert_one(food)
    
    # 4. food_code 업데이트
    # insert가 제대로 되었으면 실행
    if x:
        result = list(db.shop.find().sort('_id',-1).limit(1))
        code = result[0]['_id']
        food_code = dumps(code)[10:18] # String타입으로 형변환 및 timestamp 부분 자르기
        db.shop.update_one({'_id':code},{'$set':{'food_code':food_code}})
        return jsonify({'result': 'success'})
    else:
        return(jsonify({'result': 'insertfail'}))
       
@app.route('/fileUpload', methods=['POST'])
def fileUpload():
    f = request.files['file']
    f.save('./uploads/' + secure_filename(f.filename))
    files = os.listdir("./uploads")
    # print(f)
    
@app.route('/login')
def loginPage():
    return render_template('login.html')

# 회원가입 데이터 입력
@app.route('/insert')
def insertPage():
    return render_template('login.html')

@app.route('/insert', methods=['POST'])
def insertInfo():
     # 1. 클라이언트로부터 데이터를 받기
    username_receive = request.form['username_give']  # 클라이언트로부터 username을 받는 부분
    id_receive = request.form['id_give']  # 클라이언트로부터 id를 받는 부분
    password_receive = request.form['password_give']  # 클라이언트로부터 pw를 받는 부분

    userinfo = {
                'username' : username_receive,
                'id' : id_receive,
                'password' : password_receive
            }

    db.users.insert_one(userinfo)

    return jsonify({'result': 'success'})

# 로그인
@app.route('/login', methods=['POST'])
def login():
     # 1. 클라이언트로부터 데이터를 받기
    id_receive = request.form['id_give']  # 클라이언트로부터 id를 받는 부분
    password_receive = request.form['password_give']  # 클라이언트로부터 pw를 받는 부분

    find_target = db.users.find_one({'id':id_receive})

    # 로그인 할 아이디가 없을 경우
    if find_target is None :
        return jsonify({'result': 'not'})

    target_id = find_target['id']
    target_password = find_target['password']

    if(id_receive == target_id and password_receive == target_password):
        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'fail'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)