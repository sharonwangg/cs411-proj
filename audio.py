import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import xmltodict
from db import insert_audio,get_book_link
import urllib.request
import dload
import os 


def ready_audio(book_name):
	x=get_book_link(book_name)
	print(x)
	if(not os.path.exists("./static/music/"+x['book_name'])):

		os.mkdir('./static/music/'+x['book_name'])
		m= dload.save_unzip(x['audio_link'],"./static/music/"+x['book_name'])
		m= dload.save_unzip(x['audio_link'],"./static/music/")
		print(m)





def ready_():
	a=open('audio.txt')
	aa=a.read().split('\n')
	b=open('book.txt')
	bb=b.read().split('\n')
	for i in range(len(bb)):
		print(bb[i].split(', by')[0],aa[i])
		insert_audio(bb[i].split(', by')[0],aa[i])




