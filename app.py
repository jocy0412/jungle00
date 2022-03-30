from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bson.json_util import dumps
import requests
import hashlib
from datetime import *
import jwt

app = Flask(__name__)

client = MongoClient('mongodb://test:test@54.180.139.22', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmuckji  # 'dbmuckji'라는 이름의 db를 만들거나 사용합니다.

# [JWT] token secret key 값 지정
app.secret_key = "Jungle"

# 홈 화면
@app.route('/')
def home():
    return render_template('index.html')
    # To.dev : 추후 개발
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')
    #     user_info = db.users.find_one({"id": payload['id']})
        
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("index.html", msg="로그인 시간이 만료되었습니다.")) 
    # except jwt.exceptions.DecodeError: 
    #     return redirect(url_for("index.html", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/main')
def mainPage():
    return render_template('main.html')

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

# 회원가입, 고객정보 데이터 입력
@app.route('/api/register', methods=['POST'])
def insertInfo():
     # 클라이언트로부터 데이터를 받기
    username_receive = request.form['username_give']  # 클라이언트로부터 username을 받는 부분
    id_receive = request.form['id_give']  # 클라이언트로부터 id를 받는 부분
    pw_receive = request.form['pw_give']  # 클라이언트로부터 pw를 받는 부분
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() # pw 해시 처리

    userinfo = {
                'username' : username_receive,
                'id' : id_receive,
                'password' : pw_hash,
                'kor':'0',
                'cn':'0',
                'jpn':'0',
                'west':'0',
                'etc':'0'
            }

    db.users.insert_one(userinfo)

    return jsonify({'result': 'success'})

# 로그인 - id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.

@app.route('/api/login', methods=['POST'])
def api_login():
     # 클라이언트로부터 데이터를 받기
    id_receive = request.form['id_give']  # 클라이언트로부터 id를 받는 부분
    pw_receive = request.form['pw_give']  # 클라이언트로부터 pw를 받는 부분
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() # 비밀번호 hash로 처리

    # 로그인 할 아이디가 없을 경우
    target_id = db.users.find_one({'id':id_receive})
    if target_id is None :
        return jsonify({'result': 'not'})

    result = db.users.find_one({'id':id_receive, 'password': pw_hash})

    # 아이디랑 비밀번호 없을 경우
    if result is not None:
        # [JWT] payload 지정
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=3600)
        }
        # [JWT] 암호화 방식
        token = jwt.encode(payload, app.secret_key, algorithm='HS256')        
        return jsonify({'result':'success','token':token})
    else :
        return jsonify({'result':'fail','msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/list')
def menu_list():
  testUser = db.users.find_one({'id':'jocy0412'},{'_id': False}) 
  return render_template('main.html', name = testUser['username'], id = testUser['id'],
                          kor = testUser['kor'], cn = testUser['cn'], jpn = testUser['jpn'],
                          west = testUser['west'], etc = testUser['etc'], like = testUser['likecode']
                        )

@app.route('/api/show', methods=['POST'])
def show():
  testUser = db.users.find_one({'id':'jocy0412'},{'_id': False}) 
  print(testUser)
  category_receive = request.form['category_give']
  
  if category_receive == 'kor':
    if testUser['kor'] == '0':
      db.users.update_one({'id':testUser['id']},{'$set':{'kor':'1'}})
      kor = list(db.shop.find({'food_category': '한식'}, {'_id': False}))
      return jsonify({'result' : 'success', 'list' : kor, 'status': 1})
    else:
      db.users.update_one({'id':testUser['id']},{'$set':{'kor':'0'}})
      return jsonify({'result' : 'success','status': 0, 'category': '한식'})
    
  elif category_receive == 'west':  
    if testUser['west'] == '0':
      db.users.update_one({'id':testUser['id']},{'$set':{'west':'1'}})
      west = list(db.shop.find({'food_category': '양식'}, {'_id': False}))
      return jsonify({'result' : 'success', 'list' : west, 'status': 1})
    else:
      db.users.update_one({'id':testUser['id']},{'$set':{'west':'0'}})
      return jsonify({'result' : 'success','status': 0, 'category': '양식'})
  
  elif category_receive == 'cn':
    if testUser['cn'] == '0':
      db.users.update_one({'id':testUser['id']},{'$set':{'cn':'1'}})
      cn = list(db.shop.find({'food_category': '중식'}, {'_id': False}))
      return jsonify({'result' : 'success', 'list' : cn, 'status': 1})
    else:
      db.users.update_one({'id':testUser['id']},{'$set':{'cn':'0'}})
      return jsonify({'result' : 'success','status': 0, 'category': '중식'})  
  
  elif category_receive == 'jpn':
    if testUser['jpn'] == '0':
      db.users.update_one({'id':testUser['id']},{'$set':{'jpn':'1'}})
      jpn = list(db.shop.find({'food_category': '일식'}, {'_id': False}))
      return jsonify({'result' : 'success', 'list' : jpn, 'status': 1})
    else:
      db.users.update_one({'id':testUser['id']},{'$set':{'jpn':'0'}})
      return jsonify({'result' : 'success','status': 0, 'category': '일식'})  
  
  else:
    if testUser['etc'] == '0':
      db.users.update_one({'id':testUser['id']},{'$set':{'etc':'1'}})
      etc = list(db.shop.find({'food_category': '기타'}, {'_id': False}))
      return jsonify({'result' : 'success', 'list' : etc, 'status': 1})
    else:
      db.users.update_one({'id':testUser['id']},{'$set':{'etc':'0'}})
      return jsonify({'result' : 'success','status': 0, 'category': '기타'}) 


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)