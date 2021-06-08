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
def home():
    return render_template('login.html')


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

@app.route('/api/sign_up', methods=['POST'])
def api_sign_up():
	result = request.form
	_id = request.form['user-id']
	_password = request.form['user-password']
	_pw_hash = hashlib.sha256(_password.encode('utf-8')).hexdigest()
	return jsonify({'result': 'success', 'mgs': '회원가입 성공'})
	db.user.insert_one({'user_id': _id, 'password': _pw_hash})
	return jsonify({'result': 'success', 'mgs': '회원가입 성공'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
