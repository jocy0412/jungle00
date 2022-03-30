from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bson.json_util import dumps
import requests
from flask_pymongo import PyMongo
import gridfs


app = Flask(__name__)

client = MongoClient('mongodb://test:test@54.180.139.22', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmuckji  # 'dbmuckji'라는 이름의 db를 만들거나 사용합니다.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/addpage')
def addPage():
   return render_template('add.html')

@app.route('/api/add', methods=['POST'])
def addMenu():
    # 1. 클라이언트로부터 데이터를 받기
    food_receive = request.form['food_give']
    category_receive = request.form['category_give']
    shop_name_receive= request.form['shop_name_give']
    shop_address_receive= request.form['shop_address_give']
    shop_img_receive = request.form['shop_img_give']
    
    # 2. dbmuckji DB로 보낼 데이터 정리
    food = {
            'food_name': food_receive, 
            'food_category': category_receive, 
            'shop_name': shop_name_receive,
            'shop_address': shop_address_receive,
            'shop_img': shop_img_receive,
            'like':0,    
            'hate':0,    
            'food_code':0, # food_code를 0으로 세팅
            'shop_url':0
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

@app.route('/list')
def menu_list():
  return render_template('index2.html')

@app.route('/api/kor', methods=['GET'])
def show_kor():
  kor = list(db.shop.find({'food_category': '한식'}, {'_id': False}))
  return jsonify({'result' : 'success', 'kor_list' : kor})

@app.route('/api/west', methods=['GET'])
def show_west():
  west = list(db.shop.find({'food_category': '양식'}, {'_id': False}))
  return jsonify({'result' : 'success', 'west_list' : west})

@app.route('/api/cn', methods=['GET'])
def show_cn():
  cn = list(db.shop.find({'food_category': '중식'}, {'_id': False}))
  return jsonify({'result' : 'success', 'cn_list' : cn})

@app.route('/api/jp', methods=['GET'])
def show_jp():
  jp = list(db.shop.find({'food_category': '일식'}, {'_id': False}))
  return jsonify({'result' : 'success', 'jp_list' : jp})

@app.route('/api/etc', methods=['GET'])
def show_etc():
  etc = list(db.shop.find({'food_category': '기타'}, {'_id': False}))
  return jsonify({'result' : 'success', 'etc_list' : etc})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)