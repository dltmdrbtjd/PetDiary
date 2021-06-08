# 안녕안녕!
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import jwt
import hashlib
import datetime as dt

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbpetdiary

SECRET_KEY = 'PETDIARY'


@app.route('/')
def main():
    # 전부 삭제
    db.review.delete_many({})
    # 2개정도 temporary data 넣어주기
    doc1 = {'title': '타이틀1', 'content': '컨텐트1', 'create_date': 'create_date1', 'author': 'author1',
            'file_name': 'file_name1'}
    doc2 = {'title': '타이틀2', 'content': '컨텐트2', 'create_date': 'create_date2', 'author': 'author2',
            'file_name': 'file_name2'}
    db.review.insert_one(doc1)
    db.review.insert_one(doc2)

    reviews = list(db.review.find({}, {'_id': False}))
    return render_template('main.html', reviews=reviews)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'user_id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up')
def sign_up():
	return render_template('sign_up.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
