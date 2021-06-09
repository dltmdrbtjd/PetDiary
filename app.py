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


# post.html API
@app.route('/api/diary_save', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    today = datetime.now()

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    author = db.user.find_one({'user_id': payload['id']})

    doc = {
        'title':title_receive,
        'content':content_receive,
        'date':today.strftime('%Y-%m-%d-%H-%M-%S'),
        'author':author['user_id']
    }

    db.pet_diary.insert_one(doc)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
