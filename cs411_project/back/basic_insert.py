import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import hashlib 
import flask
from flask import request

def login(username,password):
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='cs411',
	                             db='book_club')
	try: 
		with connection.cursor() as cur:
			cur.execute('Select username,email,age from login where username = %s and password = %s', ( username, password)) 
			rows = cur.fetchall()
			if(len(rows)==0):
				print('wrong Username or password')
			else:
				for i in rows:
					print('Username :'+i[0])
					print('email :'+i[1])
					print('age :'+str(i[2]))


	finally:
	    connection.close()



def create_user(username,password,email,age):
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='cs411',
	                             db='book_club')

	try:
	    with connection.cursor() as cursor:
	        sql = "INSERT INTO `user` (`username`) VALUES (%s)"
	        cursor.execute(sql, (username))
	        #password_hash= hashlib.md5(password).hexdigest() 
	        sql = "INSERT INTO `login` (`username`,`password`,`email`,`age`) VALUES (%s,%s,%s,%s)"
	        cursor.execute(sql, (username,password,email,age))
	    connection.commit()
	finally:
	    connection.close()





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


def delete(value):
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='cs411',
	                             db='book_club')

	try:
	    with connection.cursor() as cursor:
	        sql = "delete from `post` where post_id=(%s)"
	        cursor.execute(sql, (value))
	    connection.commit()
	finally:
	    connection.close()


	

def search(value):
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='cs411',
	                             db='book_club')



	try: 

	    with connection.cursor() as cur:

	            
	        cur.execute('Select username, text1,dateTime from post where text1 like %s or username like %s', ("%" + value + "%","%" + value + "%")) 
	        rows = cur.fetchall()
	        for i in rows:
		        print('Username :'+i[0])
		        print('text :'+i[1])
		        print('dateTime :'+str(i[2]))



	finally:
	    connection.close()




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






app = flask.Flask("__main__", template_folder= 'templates/')
@app.route('/')
def index():
	return flask.render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def loginpage():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		age = request.form['age']
		password = request.form['password']
		create_user(username, password,email,age)
		print(username, email, age, password)
		return flask.render_template("index.html")
	return flask.render_template("index.html")

app.run(debug = True)
