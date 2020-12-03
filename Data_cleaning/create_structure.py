import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import time
import xmltodict

a= open('link_list.txt')
bb= open('audio1.txt','w+')
re=a.read().split('\n')
for i in re:
	re1=' '.join(i.split('https://librivox.org/')[1].split('by')[0].split('-')[:-1])
	x = requests.get(i)
	y=json.loads(json.dumps(x.text))
	print(y.split('<dt>Whole book (zip file)</dt>')[1].split('" class="book-download-btn">Download</a></dd>')[0].split('<dd><a href="')[1]+'\n')
	bb.write(y.split('<dt>Whole book (zip file)</dt>')[1].split('" class="book-download-btn">Download</a></dd>')[0].split('<dd><a href="')[1]+'\n')
	time.sleep(10)




#aaa='https://librivox.org/search?q=the%20power%20of%20word&search_form=advanced'
#aaa='https://librivox.org/the-hound-of-the-baskervilles-by-arthur-conan-doyle/'
#x = requests.get(aaa)
#y=json.loads(json.dumps(x.text))
#bb.write(y)
#bb.write(y.split('<dt>Whole book (zip file)</dt>')[1].split('" class="book-download-btn">Download</a></dd>')[0].split('<dd><a href="')[1])


#bb.close()
#https://librivox.org/search?q=The%20Hound%20of%20the%20Baskervilles&search_form=advanced
#http://www.archive.org/download/hound_baskervilles_librivox/hound_baskervilles_librivox_64kb_mp3.zip