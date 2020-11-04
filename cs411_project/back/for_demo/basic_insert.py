import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import hashlib 
import flask
from flask import Flask, render_template, request,url_for, redirect,session
import pymysql.cursors
from datetime import date

app = Flask(__name__)

app.secret_key = 'Team105'

def log_me_in(username,password):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    returni=[]
    try: 
        with connection.cursor() as cur:
            cur.execute('Select username,email,age from login where username = %s and password = %s', ( username, password)) 
            rows = cur.fetchone()
            returni=rows

    finally:
        connection.close()
        return returni


def show_post():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    returni=[]

    try: 

        with connection.cursor() as cur:

                
            cur.execute('Select username, text1,dateTime,post_id from post') 
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni



def create_user(username,password,email,age):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    value=''

    print(username)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user` (`username`) VALUES (%s)"
            cursor.execute(sql, (username))
            #password_hash= hashlib.md5(password).hexdigest() 
            sql = "INSERT INTO `login` (`username`,`password`,`email`,`age`) VALUES (%s,%s,%s,%s)"
            value=cursor.execute(sql, (username,password,email,age))
        connection.commit()
    finally:
        connection.close()
        print(value)
        return value





def create_post(username,text,date,book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `post` (`username`,`text1`, `dateTime`,`book_id`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username,text,'2020-01-01','12'))
        connection.commit()
    finally:
        connection.close()


def delete_record(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')
    print('a')

    try:
        with connection.cursor() as cursor:
            sql = "delete from `post` where post_id=(%s)"
            cursor.execute(sql, (value))
        print('dafd')
        connection.commit()
    finally:
        connection.close()


    

def search_me(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')
    returni=[]
    try: 

        with connection.cursor() as cur:

                
            cur.execute('Select username, text1,dateTime from post where text1 like %s or username like %s', ("%" + value + "%","%" + value + "%")) 
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni


def edit_helper(post_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    returni=[]

    try: 

        with connection.cursor() as cur:

                
            cur.execute('Select username, text1,dateTime,post_id from post where post_id=%s', post_id) 
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni



def edit(post_id,value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "update `post` set text1=%s where post_id=%s"
            cursor.execute(sql, (value,str(post_id)))
        connection.commit()
    finally:
        connection.close()


def can_delete(id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')
    returni=''
    try: 

        with connection.cursor() as cur:

                
            cur.execute('Select username from post where post_id=%s', str(id)) 
            rows = cur.fetchone()
            returni=rows[0]
    finally:
        connection.close()
        return True if(returni==session['username']) else False






def show_user(username):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='admin',
                                 db='book_club')

    returni=[]

    try: 

        with connection.cursor() as cur:

                
            cur.execute('Select username,email,age from login where username=%s',username) 
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni



@app.route('/', methods=['POST', 'GET'])
def index():
    if 'loggedin' not in session:
        return redirect('/login')



    values=show_post()
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            print(date.today())
            create_post(session['username'],task_content,date.today(),'12')
            #val=show_post()
            return redirect('/home')
        except:
            return 'There was an issue adding your data'


    else:
        values=show_post()
        return render_template('home.html', tasks=values)


@app.route('/delete/<int:id>')
def delete(id):
    print(session['username'])
    print(can_delete(id))
    if(not can_delete(id)):
        return redirect('/')
    try:
        delete_record(str(id))
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print(session['username'])
    print(can_delete(id))
    if(not can_delete(id)):
        return redirect('/')

    value=edit_helper(id)
    if request.method == 'POST':
        val= request.form['content']

        try:
            edit(id,val)
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=value)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account=log_me_in(username,password)
        if account:
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = account[0]
            return render_template('home.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']
        print(age)
        val=create_user(username,password,email,age)
        if val==1:
            msg='User created successfully'
        else:
            msg="Please choose another username"
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)



@app.route('/home')
def home():
    if 'loggedin' in session:
        val=show_post()
        return render_template('home.html', username=session['username'],tasks=val)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        account=show_user(session['username'])
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        value = request.form['book']
        returns=search_me(value)
        if len(returns) == 0:
            return render_template('home.html', msg='No such posts')
        else:
            return render_template('home.html',msg='These are the records',tas=returns)

    return render_template('home.html')









if __name__ == "__main__":
    app.run(debug=True)
