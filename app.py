# 안녕안녕!
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import hashlib
import datetime as dt
from datetime import datetime
from bson.objectid import ObjectId
import os

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbpetdiary

SECRET_KEY = 'PETDIARY'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect("main")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        reviews = list(db.reviews.find({}).sort("date", -1))
        return render_template('main.html', reviews=reviews)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


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


def isDuplicate(_id):
    if db.user.find_one({'user_id': _id}):
        return True
    return False


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/api/sign_up', methods=['POST'])
def api_sign_up():
    result = request.form
    _id = request.form['user-id']
    if isDuplicate(_id):
        return jsonify({'success': False, 'msg': '중복된 아이디입니다.'})
    _password = request.form['user-password']
    _pw_hash = hashlib.sha256(_password.encode('utf-8')).hexdigest()
    db.user.insert_one({'user_id': _id, 'password': _pw_hash})
    return jsonify({'success': True, 'msg': '로그인 페이지로 이동합니다.'})

@app.route('/api/diary_check', methods=['POST'])
def diary_check():
    token_receive = request.form['token_give']['id']
    author_receive = request.form['author_give']

    payload_receive = jwt.decode(token_receive,SECRET_KEY,algorithms='HS256')
    payload_encoded = jwt.encode(payload_receive,SECRET_KEY,algorithm='HS256')

    author_token = payload_receive['id']

    if author_token == author_receive and token_receive == payload_encoded:
        return jsonify({'result':'success', 'msg':'ㅎㅇㅎㅇ'}, payload_encoded=payload_encoded)
    else:
        return jsonify({'result':'fail', 'msg':'ㄴㄴ'})

@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/api/diary_save', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    save_to = f'static/images/{filename}.{extension}'
    file.save(save_to)

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    author = db.user.find_one({'user_id': payload['id']})

    doc = {
        'title': title_receive,
        'content': content_receive,
        'date': today.strftime('%Y-%m-%d %H:%M'),
        'author': author['user_id'],
        'file': f'images/{filename}.{extension}'
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '작성완료!'})


@app.route('/api/valid_to_delete', methods=['POST'])
def api_valid():

    token_receive = request.form['token_give']
    author_receive = request.form['id_give']

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        if payload['id'] == author_receive:

            return jsonify({'result': 'success', 'is_authorized': 'True'})
        else:
            return jsonify({'result': 'success', 'is_authorized': 'False'})
        # userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        # return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/api/delete_by__id', methods=['POST'])
def api_delete():

    _id_receive = request.form['_id_give']

    file_name = db.reviews.find_one({'_id': ObjectId(_id_receive)})['file']
    os.remove('static/'+file_name)
    db.reviews.delete_one({'_id': ObjectId(_id_receive)})

    return jsonify({'msg': '삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
