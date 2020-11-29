#built using tutorials:
#https://www.codementor.io/@garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
#https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/

import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import hashlib
import flask
from flask import Flask, render_template, request,url_for, redirect,session
from db import  save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages,get_id
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'Team105'

def log_me_in(username,password):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
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
                                 password='cs411',
                                 db='book_club')

    returni=[]

    try:

        with connection.cursor() as cur:


            cur.execute('Select p.username, p.text1,p.dateTime,p.post_id, b.book_title from post p natural join books b order by dateTime desc')
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def get_posts(g_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    returni=[]

    try:

        with connection.cursor() as cur:


            cur.execute('Select distinct p.username, p.text1,p.dateTime,p.post_id, b.book_title from post p natural join books b join Group_ g on g.book_id = b.book_id where g.group_id = %s order by dateTime desc',(g_id))
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def create_user(username,password,email,age):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
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
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `post` (`username`,`text1`, `dateTime`,`book_id`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username,text,date,book_id))
        connection.commit()
    finally:
        connection.close()


def delete_record(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
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
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select p.username, p.text1,p.dateTime,p.post_id, b.book_title from post p natural join books b where p.text1 like %s or p.username like %s or b.book_title like %s or b.author like %s order by dateTime desc', ("%" + value + "%","%" + value + "%", "%" + value + "%", "%" + value + "%"))
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni


def search_g_posts(value,g_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select p.username, p.text1,p.dateTime,p.post_id, b.book_title from post p natural join books b join Group_ g on g.book_id = b.book_id where (p.text1 like %s or p.username like %s or b.book_title like %s or b.author like %s) and g.group_id = %s order by dateTime desc', ("%" + value + "%","%" + value + "%", "%" + value + "%", "%" + value + "%", g_id))
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni


def search_book(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select book_id from books where book_title like %s limit 1', ("%" + value + "%"))
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni

def book_id_to_name(book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select book_title, author from books where book_id=%s', book_id)
            rows = cur.fetchone()
            returni=rows


    finally:
        connection.close()
        return returni


def edit_helper(post_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
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
                                 password='cs411',
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
                                 password='cs411',
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
                                 password='cs411',
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


def start_reading(username, book_id, page_number):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `Reads` (`username, book_id, page_number`) VALUES (%s, %s, %s)"
            cur.execute(sql, (username, book_id, page_number))
        connection.commit()
    finally:
        connection.close()


def update_page_number(username, book_id, page_number):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "UPDATE `Reads` SET page_number = %s WHERE username = %s AND book_id = %s"
            cur.execute(sql, (page_number, username, book_id))
        connection.commit()
    finally:
        connection.close()


def leave_group(username, group_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "DELETE FROM `Group_` WHERE username = %s AND group_id = %s"
            cur.execute(sql, (username, group_id))
        connection.commit()
    finally:
        connection.close()

def start_reading(username, book_id, page_number):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `Reads` (`username, book_id, page_number`) VALUES (%s, %s, %s)"
            cur.execute(sql, (username, book_id, page_number))
        connection.commit()
    finally:
        connection.close()


def stop_reading(username, book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "DELETE FROM `Reads` WHERE username = %s AND book_id = %s"
            cur.execute(sql, (username, book_id))
        connection.commit()
    finally:
        connection.close()

def like_helper(user,bookid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try:
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM Likes WHERE EXISTS(SELECT * FROM `Likes` WHERE username = %s AND book_id = %s)', (user, bookid))
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        if returni.len == 0:
            return False
        else:
            return True

def like(user, bookid, like=True):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = ""
            if like:
                if like_helper(user, bookid):
                    sql = "UPDATE `Likes` SET likes_dislikes = 'Like' WHERE username = %s AND book_id = %s"
                else:
                    sql = "INSERT INTO `Likes` (`username`, `book_id`, `likes_dislikes`) VALUES (%s, %s, 'Like')"
            else:
                if like_helper(user, bookid):
                    sql = "UPDATE `Likes` SET likes_dislikes = 'Dislike' WHERE username = %s AND book_id = %s"
                else:
                    sql = "INSERT INTO `Likes` (`username`, `book_id`, `likes_dislikes`) VALUES (%s, %s, 'Dislike')"
        cur.execute(sql, (user, bookid))
        connection.commit()
    finally:
        connection.close()


#book club functions

#event functions are available to all users
def add_event(date, e_name, e_desc, e_loc, group_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Event_` (`dateTime`,`event_name`,`event_description`,`location`,`group_id`) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (date, e_name, e_desc, e_loc, group_id))
        connection.commit()
    finally:
        connection.close()

def search_events(value,g_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try: 
        with connection.cursor() as cur:   
            cur.execute('Select event_id, dateTime, event_name, event_description, location from Event_ where (event_name like %s or event_description like %s or location like %s) and group_id = %s order by dateTime desc', ("%" + value + "%","%" + value + "%", "%" + value + "%", g_id)) 
            rows = cur.fetchall()
            returni=rows

    finally:
        connection.close()
        return returni


def delete_event(ev_id):
    #check if superuser of group, then allow delete or not delete - need to rework book_club table to select superuser
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `Event_` WHERE event_id=(%s)"
            cursor.execute(sql, (ev_id))
        connection.commit()
    finally:
        connection.close()

def edit_helper_event(ev_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try: 
        with connection.cursor() as cur:
            cur.execute('Select event_id, dateTime, event_name, event_description, location from Event_ where event_id=%s', ev_id) 
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def edit_event(date, loc, ev_name, ev_desc, ev_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Event_ SET dateTime=%s, location=%s, event_name=%s, event_description=%s WHERE event_id=%s"
            cursor.execute(sql, (date, loc, ev_name, ev_desc, str(ev_id)))
        connection.commit()
    finally:
        connection.close()


#timeline functions are only available to superusers
def add_timeline_event(date, chap):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `timeline` (dateTime, chapter) VALUES(%s,%s)"
            cursor.execute(sql, (date, chap))
        connection.commit()
    finally:
        connection.close()

def delete_timeline_event(time_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM timeline WHERE timeline_id=(%s)"
            cursor.execute(sql, (time_id))
        connection.commit()
    finally:
        connection.close()

def edit_helper_timeline(time_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]
    try: 
        with connection.cursor() as cur:
            cur.execute('Select dateTime, chapter from timeline where timeline_id=%s', time_id) 
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def edit_timeline(date, chap, timeid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Event_ SET dateTime=%s, chapter=%s, WHERE timeline_id=%s"
            cursor.execute(sql, (date, chap, str(timeid)))
        connection.commit()
    finally:
        connection.close()


def get_groups(username):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select group_id from Group_ where username=%s', username)
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def get_group(username):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select username,group_id,book_id,super_user from Group_ where username=%s', username)
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def new_group(username,book_id,super_user):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Group_` (`username`,`book_id`,`super_user`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username,book_id,super_user))
        connection.commit()
    finally:
        connection.close()

def get_group_members(group_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select username from Group_ where group_id=%s', group_id)
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def get_group_byid(group_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('select * from Group_ where group_id = %s',group_id)
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni  

def add_to_group(username,group_id,book_id,super_user):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Group_` (`username`,`group_id`,`book_id`,`super_user`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username,group_id,book_id,super_user))
        connection.commit()
    finally:
        connection.close()

def show_events(group_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='cs411',
                                 db='book_club')

    returni=[]

    try:

        with connection.cursor() as cur:


            cur.execute('Select * from Event_ where group_id = %s order by dateTime desc', group_id)
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'loggedin' not in session:
        return redirect('/login')

    values = []
    events = []
    usr = session['username']
    groups = get_groups(usr)
    for group in groups :
        values += get_posts(group[0])
        events += show_events(group[0])
    return render_template('home.html', tasks = values, usr = session['username'], events = events)
        


@app.route('/delete/<int:g_id>/<int:id>')
def delete(g_id, id):
    print(session['username'])
    print(can_delete(id))
    if(not can_delete(id)):
        return redirect(url_for('group', g_id=g_id))
    try:
        delete_record(str(id))
        return redirect(url_for('group', g_id=g_id))
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:g_id>/<int:id>', methods=['GET', 'POST'])
def update(g_id, id):
    print(session['username'])
    print(can_delete(id))
    if(not can_delete(id)):
        return redirect(url_for('group', g_id=g_id))

    value=edit_helper(id)
    if request.method == 'POST':
        val= request.form['content']

        try:
            edit(id,val)
            return redirect(url_for('group', g_id=g_id))
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=value, group_id = g_id)


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
            values = []
            usr = session['username']
            groups = get_groups(usr)
            for group in groups :
                values += get_posts(group[0])
            return render_template('home.html',tasks=values, usr = session['username'])
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
        values = []
        events = [] 
        usr = session['username']
        groups = get_groups(usr)
        for group in groups :
            values += get_posts(group[0])
            events += show_events(group[0])
        return render_template('home.html', usr=session['username'],tasks=values, events = events)
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
        if value == "" or len(returns) == 0:
            return render_template('home.html', usr = session['username'], msg='No records for "' + value + '"')
        else:
            return render_template('home.html',msg='Records returned by search for "' + value + '"',tasks=returns, usr = session['username'])


@app.route('/search_group_posts/<int:g_id>', methods=['GET', 'POST'])
def search_group_posts(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[2]
    admin = group[3]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    if usr == admin:
        admin = 1
    else:
        admin = 0
    members = get_group_members(g_id)
    posts = get_posts(g_id)
    if request.method == "POST":
        value = request.form['book']
        posts=search_g_posts(value,g_id)
        if value == "" or len(posts) == 0:
            return render_template('group.html', usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = events, members = members, pmsg='No records for "' + value + '"')
        else:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = events, members = members, pmsg='Records returned by search for "' + value + '"')


@app.route('/post_group_posts/<int:g_id>', methods=['GET', 'POST'])
def post_group_posts(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[2]
    admin = group[3]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    if usr == admin:
        admin = 1
    else:
        admin = 0
    members = get_group_members(g_id)
    posts = get_posts(g_id)
    if request.method == 'POST':
        task_content = request.form['content']
        book_content = request.form['book1']
        posts = get_posts(g_id)
        if task_content == "" or book_content == "":
            return render_template('group.html', usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = events, members = members, pmsg='Post could not be added, please enter Post text and Book title')
        book_ins = search_book(book_content)
        try:
            print(datetime.now())
            create_post(session['username'],task_content,datetime.now(),book_ins)
            #val=show_post()
            return redirect(url_for('group', g_id=g_id))
        except:
            return 'There was an issue adding your data'


@app.route('/create_group/', methods=['GET', 'POST'])
def create_group():
    message = 'Please Enter the group name and book'
    if request.method == 'POST':
        group_name = request.form['group_name']
        book_content = request.form['book1']
        if group_name == "" :
            return render_template('create_group.html', msg=' Group could not be created, please enter Group name and book')
        book_ins = search_book(book_content)
        new_group(session['username'],book_ins,session['username'])
        return redirect(url_for('group_router'))

    return render_template('create_group.html', message=message)

@app.route('/join_group', methods=['GET', 'POST'])
def join_group():
    message = 'Please Enter the group id'
    if request.method == 'POST':
        group_id = request.form['group_id']
        if group_id == "":
            return render_template('join_group.html', msg='Invalid Group ID')
        val = get_group_byid(group_id)
        if(val is None):
            return render_template('join_group.html', msg='Invalid Group ID')
        add_to_group(session['username'],val[1],val[2],val[3])
        return redirect(url_for('group_router'))
    return render_template('join_group.html')


@app.route('/group_router', methods=['POST', 'GET'])
def group_router():
    usr = session['username']
    test = get_group(usr)
    val = get_groups(usr)
    if(test is None):
        return redirect(url_for('create_group'))
    return render_template('group_router.html', group_id = val)


@app.route('/group/<int:g_id>', methods=['POST', 'GET'])
def group(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[2]
    admin = group[3]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    if usr == admin:
        admin = 1
    else:
        admin = 0
    members = get_group_members(g_id)  
    posts = get_posts(g_id)
    print(posts) 
    if request.method == 'POST':
        e_name = request.form['ename']
        date = request.form['date']
        time = request.form['time']
        e_desc = request.form['desc']
        e_loc = request.form['loc']
        e_date = date + " " + time  
        events = show_events(g_id)
        if e_name == "" or date == "" or time == "" or e_desc == "" or e_loc == "":
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = events, members = members, emsg='Event could not be added, please enter valid Event data')
        add_event(e_date, e_name, e_desc, e_loc, g_id)
        return redirect(url_for('group', g_id=g_id))
    return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = events, members = members)

@app.route('/delete_event/<int:g_id>/<int:e_id>')
def delete_e(g_id,e_id):
    val = get_group(session['username'])
    if(val is None):
        return redirect(url_for('create_group'))
    # if(session['username'] != val[3]):
    #     return redirect('/group')
    try:
        delete_event(e_id)
        return redirect(url_for('group', g_id=g_id))
    except:
        return 'There was a problem deleting that task'

@app.route('/update_event/<int:g_id>/<int:e_id>', methods=['GET', 'POST'])
def update_e(g_id,e_id):
    val = get_group(session['username'])
    if(val is None):
        return redirect(url_for('create_group'))
    # if(session['username'] != val[3]):
    #     return redirect('/group')

    value=edit_helper_event(e_id)
    value = (value[0],value[1].split(" "),value[2],value[3],value[4])
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        e_date = date + " " + time
        loc = request.form['loc']
        ev_name = request.form['ename']
        ev_desc = request.form['desc']
        try:
            edit_event(e_date, loc, ev_name, ev_desc, e_id)
            return redirect(url_for('group', g_id=g_id))
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update_event.html', group_id = g_id, task=value)

@app.route('/search_event/<int:g_id>', methods=['GET', 'POST'])
def search_e(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[2]
    admin = group[3]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    if usr == admin:
        admin = 1
    else:
        admin = 0
    members = get_group_members(g_id)
    posts = get_posts(g_id)    
    if request.method == "POST":
        value = request.form['event']
        returns = search_events(value,g_id)
        if value == "" or len(returns) == 0:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = returns, members = members, emsg='No records for "' + value + '"')
        else:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], admin = admin, posts = posts, tasks = returns, members = members, emsg='Records returned by search for "' + value + '"')

@app.route('/leave_group/<int:g_id>')
def leave(g_id):
    val = get_group(session['username'])
    if(val is None):
        return redirect(url_for('create_group'))

    leave_group(session['username'], g_id)
    return redirect('/group_router')

if __name__ == "__main__":
    app.run(debug=True)
