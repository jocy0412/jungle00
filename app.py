from flask import Flask, render_template, jsonify, request # 서버 연결
from pymongo import MongoClient
from bs4 import BeautifulSoup
import simplejson as json
from bson import ObjectId
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient('mongodb://test:test@54.180.139.22', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmuckji  # 'dbmuckji'라는 이름의 db를 만들거나 사용합니다.

@app.route('/')
def home():
    return render_template('index.html')

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