import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json

'''
data={}
i=0
x= requests.get('https://openlibrary.org/data/ol_dump_latest.txt.gz')
with open('data1.txt', mode='rt') as f:

    text = f.read(1000) # Reads the first 100 character and moves pointer to 101th character

    while len(text) > 0 and i!=1000:
 
        data=data+text
        text = f.read(1000)
        i=i+1 # Move pointer to end of next 100 character


pprint.pprint(data[:1000])
book_id int,
author varchar(50),
book_title varchar(60),
genre varchar(10),
'''
a=open('data.txt')
e=a.read()
e=json.loads(e)
pprint.pprint(e['books'].keys())


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='cs411',
                             db='book_club')
'''
    with connection.cursor() as cursor:
    	sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    	cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    connection.commit()
'''
try:
    with connection.cursor() as cursor:
    	for i in e['books'].keys():
    		print(i)
    		print(e['books'][i]['title'])
    		print(e['books'][i]['authors'][0]['first_name']+' '+e['books'][i]['authors'][0]['last_name'])
    		print(e['books'][i]['genres'][0]['name'])
    		sql = "INSERT INTO `books` (`book_id`,`author`,`book_title`, `genre`) VALUES (%s, %s, %s, %s)"
    		cursor.execute(sql, (str(i),e['books'][i]['authors'][0]['first_name']+' '+e['books'][i]['authors'][0]['last_name'],e['books'][i]['title'],e['books'][i]['genres'][0]['name']))
    connection.commit()

finally:
	connection.close()