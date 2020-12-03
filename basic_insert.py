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
from db import  save_room, add_room_members, get_rooms_for_user, get_room, is_room_member,get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages,get_id,get_all_room,delete_chat
import pymysql.cursors
from datetime import datetime
from flask_socketio import SocketIO, join_room, leave_room
from datetime import datetime
import os
from audio import ready_audio
from kmeans import get_group_id_of_new_user,get_book_id_to_new_book_id,clf,clusters,group_new_user

from sklearn.cluster import KMeans

app = Flask(__name__)

app.secret_key = 'Team105'
socketio = SocketIO(app)



def in_like_table():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=''
    try:

        with connection.cursor() as cur:


            cur.execute('select username from Likes where username=%s', str(session['username']))
            rows = cur.fetchone()
            returni=rows[0]
    finally:
        connection.close()
        return True if(returni==session['username']) else False




def log_me_in(username,password):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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

def get_posts(b_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    returni=[]

    try:

        with connection.cursor() as cur:


            cur.execute('Select distinct p.username, p.text1,p.dateTime,p.post_id, b.book_title from post p natural join books b where b.book_id = %s order by dateTime desc',(b_id))
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def create_user(username,password,email,age):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('SELECT p.username, p.text1,p.dateTime,p.post_id, b.book_title FROM post p NATURAL JOIN books b WHERE p.text1 LIKE %s OR p.username LIKE %s OR b.book_title LIKE %s OR b.author LIKE %s ORDER BY dateTime DESC', ("%" + value + "%","%" + value + "%", "%" + value + "%", "%" + value + "%"))
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni

#fix this
def search_g_posts(value,b_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('SELECT p.username, p.text1,p.dateTime,p.post_id, b.book_title FROM post p NATURAL JOIN books b WHERE (p.text1 LIKE %s OR p.username LIKE %s OR b.book_title LIKE %s OR b.author like %s) AND b.book_id = %s ORDER BY dateTime DESC', ("%" + value + "%","%" + value + "%", "%" + value + "%", "%" + value + "%", b_id))
            rows = cur.fetchall()
            returni=rows



    finally:
        connection.close()
        return returni


def search_book(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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


def get_all_books():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select book_title, author, book_id from books order by book_title')
            rows = cur.fetchall()
            returni=rows


    finally:
        connection.close()
        return returni

def max_book_id():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:

        with connection.cursor() as cur:


            cur.execute('Select max(book_id) from books')
            rows = cur.fetchone()
            returni=rows


    finally:
        connection.close()
        return returni

def edit_helper(post_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
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

def start_reading(username, book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `Reads_` (`username`, `book_id`) VALUES (%s, %s)"
            cur.execute(sql, (username, book_id))
        connection.commit()
    finally:
        connection.close()


def stop_reading(username, book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    try:
        with connection.cursor() as cur:
            sql = "DELETE FROM `Reads_` WHERE username = %s AND book_id = %s"
            cur.execute(sql, (username, book_id))
        connection.commit()
    finally:
        connection.close()

def stop_reading_check(username, book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:
        with connection.cursor() as cur:
            sql = "Select * FROM `Reads_` WHERE `username` = %s AND `book_id` = %s"
            cur.execute(sql, (username, book_id))
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def like_helper(user,bookid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM Likes WHERE EXISTS(SELECT * FROM `Likes` WHERE username = %s AND book_id = %s)', (user, bookid))
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        if len(returni) == 0:
            return False
        else:
            return True

def get_like_dislike(user,flag):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    if flag=="Like":
        try:
            with connection.cursor() as cur:
                cur.execute('SELECT book_id FROM `Likes` WHERE `likes_dislikes`=%s and username = %s', ('Likes',user))
                rows = cur.fetchall()
                returni=rows
        finally:
            connection.close()
    else:
        try:
            with connection.cursor() as cur:
                cur.execute('SELECT `book_id` FROM `Likes` WHERE `likes_dislikes`=%s and username = %s', ('Disike',user))
                rows = cur.fetchall()
                returni=rows
        finally:
            connection.close()


    print(returni)
    return returni

def get_likes(usr):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try:
        with connection.cursor() as cur:
            cur.execute('SELECT b.book_title, l.likes_dislikes FROM Likes l NATURAL JOIN books b WHERE username = %s',usr)
            rows = cur.fetchall()
            returni = rows
    finally:
        connection.close
        return returni 



def get_book_ids():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')

    # select book_ids from Books table
    book_ids = []
    try:
        with connection.cursor() as cur:
            sql = "SELECT book_id FROM `Books`"
            cur.execute(sql)
            book_ids = cur.fetchall()
        connection.commit()
    finally:
        connection.close()

    # fix tuple problem
    fixed_book_ids = []
    for book_id in book_ids:
        fixed_book_ids.append(book_id[0])

    return fixed_book_ids

def like(user, bookid, like):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    print(user, bookid, like)

    try:
        with connection.cursor() as cur:
            sql = ""
            if like == 1:
                if like_helper(user, bookid):
                    sql = "UPDATE `Likes` SET likes_dislikes = 'Like' WHERE username = %s AND book_id = %s"
                else:
                    sql = "INSERT INTO `Likes` (`username`, `book_id`, `likes_dislikes`) VALUES (%s, %s, 'Like')"
            elif like == -1:
                if like_helper(user, bookid):
                    sql = "UPDATE `Likes` SET likes_dislikes = 'Dislike' WHERE username = %s AND book_id = %s"
                else:
                    sql = "INSERT INTO `Likes` (`username`, `book_id`, `likes_dislikes`) VALUES (%s, %s, 'Dislike')"
            elif like == 0:
                if like_helper(user, bookid):
                    sql = "delete from `Likes` WHERE username = %s AND book_id = %s"
                else:
                    return
            cur.execute(sql, (user, bookid))
        connection.commit()
    finally:
        connection.close()

#event functions are available to all users
def add_event(date, e_name, e_desc, e_loc, book_id, host):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Event_` (`dateTime`,`event_name`,`event_description`,`location`,`book_id`,`host1`) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (date, e_name, e_desc, e_loc, book_id, host))
        connection.commit()
    finally:
        connection.close()

def search_events(value,b_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try: 
        with connection.cursor() as cur:   
            cur.execute('Select event_id, dateTime, event_name, event_description, location from `Event_` where (event_name like %s or event_description like %s or location like %s) and book_id = %s order by dateTime desc', ("%" + value + "%","%" + value + "%", "%" + value + "%", b_id)) 
            rows = cur.fetchall()
            returni=rows

    finally:
        connection.close()
        return returni


def delete_event(ev_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
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
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]
    try: 
        with connection.cursor() as cur:
            cur.execute('Select `event_id`, `dateTime`, `event_name`, `event_description`, `location` from `Event_` where event_id=%s', ev_id) 
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def edit_event(date, loc, ev_name, ev_desc, ev_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `Event_` SET dateTime=%s, location=%s, event_name=%s, event_description=%s WHERE event_id=%s"
            cursor.execute(sql, (date, loc, ev_name, ev_desc, str(ev_id)))
        connection.commit()
    finally:
        connection.close()


def get_groups(username):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select book_id from `Reads_` where username=%s', username)
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def get_group(username):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select username,book_id, from `Reads_` where username=%s', username)
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni

def get_group_members(book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('Select username from `Reads_` where book_id=%s', book_id)
            rows = cur.fetchall()
            returni=rows
    finally:
        connection.close()
        return returni

def get_group_byid(book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=[]

    try:

        with connection.cursor() as cur:
            cur.execute('select * from `Reads_` where book_id = %s',book_id)
            rows = cur.fetchone()
            returni=rows
    finally:
        connection.close()
        return returni  

def show_events(book_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    returni=[]

    try:

        with connection.cursor() as cur:


            cur.execute('Select * from `Event_` where book_id = %s order by dateTime desc', book_id)
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
            events = []
            usr = session['username']
            groups = get_groups(usr)
            for group in groups :
                values += get_posts(group[0])
                events += show_events(group[0])
            return render_template('home.html',tasks=values, usr = session['username'],events=events)
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
        liked_b = []
        disliked_b = []
        likes = get_likes(session['username'])
        print(likes)
        for like in likes:
            if like[1] == 'Like':
                liked_b.append(like[0])
            elif like[1] == 'Dislike' or like[1] == 'Disike':
                disliked_b.append(like[0])
        print(liked_b)
        print(disliked_b)
        account=show_user(session['username'])
        return render_template('profile.html', account=account, dislikes = disliked_b, likes = liked_b)
    return redirect(url_for('login'))



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        value1 = request.form.get('book',False)
        groups = get_groups(session['username'])
        returns1 = []
        returns2 = []
        for group in groups:
            returns1 += search_g_posts(value1,group[0])
            returns2 += show_events(group[0])
        if value1 == "" or len(returns1) == 0:
            return render_template('home.html', usr = session['username'], msg='No records found for search',events = returns2)
        else:
            return render_template('home.html',msg='Records returned by search: ',tasks=returns1, usr = session['username'],events=returns2)

@app.route('/search_event',methods=['GET','POST'])
def search_evs():
    if request.method == "POST":
        value2 = request.form.get('event',False)
        groups = get_groups(session['username'])
        returns1 = []
        returns2 = []
        for group in groups:
            returns1 += get_posts(group[0])
            returns2 += search_events(value2,group[0])
        if value2 == "":
            return render_template('home.html',msg = 'No records found for search', tasks = returns1)
        else:
            return render_template('home.html',tasks = returns1, usr = session['username'], events=returns2)

@app.route('/search_group_posts/<int:g_id>', methods=['GET', 'POST'])
def search_group_posts(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = g_id
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    members = get_group_members(g_id)
    posts = get_posts(g_id)
    if request.method == "POST":
        value = request.form['book']
        posts=search_g_posts(value,g_id)
        if value == "" or len(posts) == 0:
            return render_template('group.html', usr = usr, group_id = g_id, book = book[0], author = book[1], posts = posts, tasks = events, members = members, pmsg='No records for "' + value + '"')
        else:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], posts = posts, tasks = events, members = members, pmsg='Records returned by search for "' + value + '"')


@app.route('/post_group_posts/<int:g_id>', methods=['GET', 'POST'])
def post_group_posts(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[1]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    members = get_group_members(g_id)
    posts = get_posts(g_id)
    if request.method == 'POST':
        task_content = request.form['content']
        #book_content = request.form['book1']
        posts = get_posts(g_id)
        if task_content == "":
            return render_template('group.html', usr = usr, group_id = g_id, book = book[0], author = book[1], posts = posts, tasks = events, members = members, pmsg='Post could not be added, please enter Post text')
        #book_ins = search_book(book_content)
        book_ins = book_id
        try:
            print(datetime.now())
            create_post(session['username'],task_content,datetime.now(),book_ins)
            #val=show_post()
            return redirect(url_for('group', g_id=g_id))
        except:
            return 'There was an issue adding your data'

#this will be broken
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

@app.route('/join_group/<int:b_id>', methods=['GET', 'POST'])
def join_group(b_id):
    val = stop_reading_check(session['username'], b_id)
    if(val is not None):
        return redirect(url_for('books'))
    start_reading(session['username'], b_id)
    return redirect(url_for('group_router'))

@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == "POST":
        books = get_all_books()
        val=[]
        for i in books:
            option = request.form[i[0]+i[1]]
            val.append(option)
        for i,book in enumerate(books):
            if(val[i] == '1'):
                print("liked", book[2])
                like(session['username'], book[2], like=1)
            elif(val[i] == '-1'):
                print("disliked" ,book[2])
                like(session['username'], book[2], like= -1)
            elif(val[i] == '0'):
                print("No Reaction",book[2])
                like(session['username'], book[2], like= 0)


        book_id_to_new_book_id = get_book_id_to_new_book_id(get_book_ids())
        gid = get_group_id_of_new_user(clf, clusters, session['username'], get_like_dislike(session['username'],'Like'), get_like_dislike(session['username'],'DisLike'), book_id_to_new_book_id)
        group_new_user(session['username'],gid)
        room_id=get_id(gid)['_id']
        add_room_members(room_id, gid, [session['username']], 'system')
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        books = get_all_books()
        return render_template('view_room.html',username=session['username'],room=gid,room_members=room_members,books=books,messages=messages)
    else:
        books = get_all_books()
        return render_template('books.html', books = books)

@app.route('/group_router', methods=['POST', 'GET'])
def group_router():
    usr = session['username']
    test = get_group(usr)
    val = get_groups(usr)
    if(test is None):
        return redirect(url_for('books'))
    return render_template('group_router.html', group_id = val)


@app.route('/group/<int:g_id>', methods=['POST', 'GET'])
def group(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[1]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
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
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], posts = posts, tasks = events, members = members, emsg='Event could not be added, please enter valid Event data')
        add_event(e_date, e_name, e_desc, e_loc, g_id, usr)
        return redirect(url_for('group', g_id=g_id))
    return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1], posts = posts, tasks = events, members = members)

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
        return 'There was a problem deleting that event'

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
            return 'There was an issue updating your event'

    else:
        return render_template('update_event.html', group_id = g_id, task=value)

@app.route('/search_event/<int:g_id>', methods=['GET', 'POST'])
def search_e(g_id):
    usr = session['username']
    group = get_group_byid(g_id)
    book_id = group[1]
    book = book_id_to_name(book_id)
    events = show_events(g_id)
    members = get_group_members(g_id)
    posts = get_posts(g_id)    
    if request.method == "POST":
        value = request.form['event']
        returns = search_events(value,g_id)
        if value == "" or len(returns) == 0:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1],  posts = posts, tasks = returns, members = members, emsg='No records for "' + value + '"')
        else:
            return render_template('group.html',  usr = usr, group_id = g_id, book = book[0], author = book[1],  posts = posts, tasks = returns, members = members, emsg='Records returned by search for "' + value + '"')

@app.route('/leave_group/<int:g_id>')
def leave(g_id):
    val = stop_reading_check(session['username'], g_id)
    if(val is None):
        return redirect(url_for('books'))

    stop_reading(session['username'], g_id)
    return redirect(url_for('group_router'))





'''
@app.route('/create-room/', methods=['GET', 'POST'])
def create_room():
    message = 'Please Enter the room_name and memebers'
    if request.method == 'POST':
        room_name = request.form['room_name']
        book_id=get_group(session['username'])[2]
        group_id=get_group(session['username'])[1]
        members = get_group_members(group_id)
        members=[i[0] for i in members]
        print(members)
        book_name=book_id_to_name(book_id)

        user_list=request.form['members'].split(',')
        usernames = [username.strip() for username in user_list]
        for i in usernames:
            if i not in members:
                return render_template('create_room.html', message='The member '+i +'is not in this group please add them')
            if i==session['username']:
                return render_template('create_room.html', message='Please add someone in the group other than yourself')

        ready_audio(book_name[0])
        room_id = save_room(room_name, session['username'],book_name)

        add_room_members(room_id, room_name, usernames, session['username'])
        return redirect(url_for('view_room', room_id=room_name))

    return render_template('create_room.html', message=message)

'''

@app.route('/rooms')
def view_room():
    if(in_like_table()):    
        room_name=get_all_room(session['username'])
        print(room_name)
        room_id=get_id(room_name['room_name'])
        room = get_room(room_id['_id'])
        room_members = get_room_members(room_id['_id'])
        books = get_all_books()
        print(room_id)
        print(room_members)
        messages = get_messages(room_id['_id'])
        #book_id=get_group(session['username'])[2]
        #book_name=book_id_to_name(book_id)
        songs ='' #os.listdir('./static/music/'+book_name[0])
        return render_template('view_room.html', username=session['username'], room=room, room_members=room_members,songs=songs,
                                messages=messages, books=books)

    else:
        books = get_all_books()
        return render_template('books.html', books=books)


@app.route('/audio/books',methods=['POST', 'GET'])
def audio_book():
    if request.method == 'POST':
        book_name=request.form.get('books',None)
        room_name=get_all_room(session['username'])
        print(room_name)
        room_id=get_id(room_name['room_name'])
        room = get_room(room_id['_id'])
        room_members = get_room_members(room_id['_id'])
        books = get_all_books()
        print(room_id)
        print(room_members)
        messages = get_messages(room_id['_id'])
        ready_audio(book_name)
        songs =os.listdir('./static/music/'+book_name)
        return render_template('view_room.html', username=session['username'], room=room, room_members=room_members,songs=songs,
                                    messages=messages, books=books)
    else:
        room_name=get_all_room(session['username'])
        print(room_name)
        room_id=get_id(room_name['room_name'])
        room = get_room(room_id['_id'])
        room_members = get_room_members(room_id['_id'])
        books = get_all_books()
        print(room_id)
        print(room_members)
        messages = get_messages(room_id['_id'])
        #book_id=get_group(session['username'])[2]
        #book_name=book_id_to_name(book_id)
        songs ='' #os.listdir('./static/music/'+book_name[0])
        return render_template('view_room.html', username=session['username'], room=room, room_members=room_members,songs=songs,
                                    messages=messages, books=books)



@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])




if __name__ == "__main__":
    socketio.run(app, debug=True)