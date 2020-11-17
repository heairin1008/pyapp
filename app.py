from flask import Flask, render_template, request, redirect
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, db='pyapp', user='root', password='java1004')
print(conn)

app = Flask(__name__)

#4. msg 수정
# if GET / POST 분기
# GET -> SELECT 쿼리 하나 -> fetchone
# POST -> update set
@app.route('/update_msg', methods=['GET','POST'])
def update_msg():
    if request.method == 'GET':
        msg_id = request.args.get('msg_id')
        cursor = conn.cursor()
        cursor.execute('SELECT msg_text FROM msg WHERE msg_id = %s', [msg_id])
        msgOne = cursor.fetchone()
        return render_template('update_msg.html', msgOne = msgOne, msg_id = msg_id)
    elif request.method == 'POST':
        msg_id = request.form['msg_id']
        msg_text = request.form['msg_text']
        cursor = conn.cursor()
        cursor.execute('UPDATE msg SET msg_text = %s WHERE msg_id = %s', [msg_text, msg_id])
        conn.commit()
        return redirect('/')

#3. msg 삭제
@app.route('/del_msg', methods=['GET'])
def del_msg():
    msg_id = request.args.get('msg_id')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM msg WHERE msg_id = %s', [msg_id])
    conn.commit()
    return redirect('/')

#2. msg_add.html 폼
@app.route('/add_msg', methods=['GET', 'POST'])
def add_msg():
    if request.method == 'GET':
        return render_template('add_msg.html')
    elif request.method == 'POST':
        msg_text = request.form['msg_text']
        # db 입력
        cursor = conn.cursor()
        cursor.execute('INSERT INTO msg(msg_text) VALUES(%s)', [msg_text])
        conn.commit
        return redirect('/')

#1. msg 목록
@app.route('/', methods=['GET'])
def msg_list():
    cursor = conn.cursor()
    cursor.execute('SELECT msg_id, msg_text FROM msg')
    msglist = cursor.fetchall()
    print(msg_list)
    return render_template('msg_list.html', msglist = msglist)

app.run(host='127.0.0.1', port=80)
#2. 