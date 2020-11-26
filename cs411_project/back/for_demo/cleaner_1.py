import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import xmltodict
import ast

a= open('json.txt')
aa= a.read()
aaa=ast.literal_eval(aa)
a.close()
b=open('query.txt','w+')
c= open('book.txt')
cc=(c.read().split('\n'))
c.close()
author_name={}
for i in cc:
    author_name[i.split(', by')[0]]=i.split(', by')[1]
pre='Insert into books values('
j=367
print(author_name.keys())
for i in aaa.keys():
    genre=''
    y = json.loads(aaa[i])
   # print(y['docs'][1].keys())
    if len(y['docs'])==0:
        continue
    else:
        if 'subject' not in y['docs'][0].keys():
            if 'subject' not in y['docs'][1].keys():
                if 'subject' not in y['docs'][2].keys():
                    if 'subject' not in y['docs'][3].keys():
                        print(i)
                    else:
                        genre=y['docs'][3]['subject'][:5]
                else:
                    genre=y['docs'][2]['subject'][:5]

            else:
                genre=y['docs'][1]['subject'][:5]

        else:
            genre=y['docs'][0]['subject'][:5]


            #print(y['docs'][0].keys())

            p=1#rint(y['docs'][0]['title_suggest'])

    if(i.strip() in author_name.keys()):
        b.write(pre+"'"+str(j)+"', '"+author_name[i.strip()]+"', '"+i+"', '"+''.join(genre)+"');\n")
        j=j+1
    else:
        if(i.split(' (')[0].strip() in author_name.keys()):
            b.write(pre+"'"+str(j)+"', '"+author_name[i.split(' (')[0].strip()]+"', '"+i+"', '"+''.join(genre)+"');\n")
            j=j+1
        else:
            if(i.split("'")[0]+i.split("'")[1] in author_name.keys()):
                b.write(pre+"'"+str(j)+"', '"+author_name[i.split("'")[0]+i.split("'")[1]]+"', '"+i+"', '"+' '.join(genre)+"');\n")


print('The Three Musketeer' in author_name.keys())
