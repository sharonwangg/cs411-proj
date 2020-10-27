import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json



connection = pymysql.connect(host='localhost',
                             user='root',
                             password='admin',
                             db='book_club')

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `post` (`username`,`post_id`,`text1`, `dateTime`,`book_id`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, ('batman','123','dgrsdgdsf','2019-01-01','12'))
    connection.commit()
finally:
    connection.close()


