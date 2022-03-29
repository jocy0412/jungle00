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

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)