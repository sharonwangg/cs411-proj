import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json

import flask

app = flask.Flask("__main__")

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='cs411',
                             db='book_club')

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `post` (`username`,`text1`, `dateTime`,`book_id`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, ('robin','dgrsdgdsf','2019-01-01','12'))
    connection.commit()
finally:
    connection.close()

@app.route("/")
def my_index():
    return flask.render_template("index.html", token = "hello")

app.run(debug = True)
