#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import mysql.connector
from datetime import datetime
from keywordQuery import query


# In[2]:


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jobscraper"
)


# In[3]:


listkeyword=query()


# In[4]:


def offreemploi(key):
    list=[]
    url='https://www.offre-emploi.tn/page/1/?s=java&region&secteur'
    url=url.replace('java',key)
    old_x='1'
    for x in range(1,5):
        url=url.replace(old_x, str(x))
        old_x=str(x)
        offreemploi=requests.get(url)
        src=bs(offreemploi.content,'html.parser')
        print(url)
        jobs=src.find_all('article',class_='js_result_row')
        for job in jobs:
            try:
                titre = job.find('span',itemprop='title').text
            except:
                titre='NULL'
            try:
                link=job.find('h2').a['href']
            except:
                link='NULL'
            try:
                location=job.find('span',itemprop="name").text
            except:
                location='NULL'
            try:
                discrip=job.find('div',itemprop="description").text.strip()
            except:
                discrip='NULL'
            try:
                date=job.find('time',itemprop="datePosted").text
            except:
                date='NULL'
            if(link != 'NULL'):
                profi=profilscraper(link)
                dict={
                    'title':titre,
                    'link':link,
                    'location':location,
                    'description':discrip,
                    'date':date,
                    'info1':profi['Detail Info 1'],
                    'info2':profi['Detail Info 2'],
                    'info3':profi['Detail Info 3'],
                    'info4':profi['Detail Info 4'],
                    'info5':profi['Detail Info 5'],
                    'info6':profi['Detail Info 6'],
                    'info7':profi['Detail Info 7']

                }
                449
                list.append(dict)
    return list


# In[5]:


def profilscraper(link):
    detail=requests.get(link)
    src2=bs(detail.content,'html.parser')
    try:
        info1=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info1=re.sub(r'(\s+|\n)',' ',info1)
    except:
        info1='NULL'
    try:    
        info2=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info2=re.sub(r'(\s+|\n)',' ',info2)
    except:
        info2='NULL'
    try:
        info3=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info3=re.sub(r'(\s+|\n)',' ',info3)
    except:
        info3='NULL'
    try:
        info4=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info4=re.sub(r'(\s+|\n)',' ',info4)
    except:
        info4='NULL'
    try:
        info5=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info5=re.sub(r'(\s+|\n)',' ',info5)
    except:
        info5='NULL'
    try:
        info6=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info6=re.sub(r'(\s+|\n)',' ',info6)
    except:
        info6='NULL'
    try:
        info7=src2.find('div',class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ','').strip()
        info7=re.sub(r'(\s+|\n)',' ',info7)
    except:
        info7='NULL'
    profildictio={
        'Detail Info 1':info1,
        'Detail Info 2':info2,
        'Detail Info 3':info3,
        'Detail Info 4':info4,
        'Detail Info 5':info5,
        'Detail Info 6':info6,
        'Detail Info 7':info7,
    }
    return profildictio   


# In[ ]:

def emploiscraper():
    for lk in listkeyword:
        list=offreemploi(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO offreemploi(title , link , location , description , date , info1, info2, info3, info4, info5, info6, info7,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['location'],l['description'],l['date'],l['info1'],l['info2'],l['info3'],l['info4'],l['info5'],l['info6'],l['info7'],lk['keyword'],now)
            try:
                mycursor.execute(sql,values)
                #mydb.commit()
            except:
                pass


# In[ ]:





# In[ ]:




