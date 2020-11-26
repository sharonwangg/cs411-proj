import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import xmltodict


a= open('book.txt')
b= open('json.txt','w+')
aa=(a.read().split('\n'))
a.close()
book_name=[]
author_name=[]
for i in aa:
	book_name.append(i.split(', by')[0])
	author_name.append(i.split(', by')[1])

di={}
for i in book_name:
	#aaa='http://openlibrary.org/search.json?q='+i
	x = requests.get(aaa)
	y=json.loads(json.dumps(x.text))
	di[i]=y
	print(x)
	if x==404:
		print(a)
b.write(str(di))
'''
qqqq= dict({"name":"Felix Klein"})
aaa='http://openlibrary.org/search.json?q=Romeo and Juliet'
x = requests.get(aaa)
print(x.text)
'''