#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import mysql.connector
from datetime import datetime
from keywordQuery import query


# In[9]:


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jobscraper"
)


# In[10]:


listkeyword=query()


# In[11]:


def nexturl(url,x):
    if x==1:
        url=url+'/page/'+str(x)
    else:
        url=url[:-1]
        url=url+str(x)
    
    return url


# In[12]:


def scrapertunitrav(key):
    list=[]
    url='https://www.tunisietravail.net/search/symfony'
    url=url.replace('symfony',key)
    tunisietravail=requests.get(url)
    src=BeautifulSoup(tunisietravail.content,'html.parser')
    for x in range(1,3):
        url=nexturl(url,x)
        print(url)
        jobs=src.find_all('div',style=lambda value: value and 'float:left;width:347px; border:solid 1px #e2e2e2; min-height:250px;margin-top:5px; margin-bottom:5px; margin-right:5px; margin-left:5px;padding-top:5px; padding-bottom:5px; padding-right:5px; padding-left:5px;' in value)
        for job in jobs:
            titre=job.find('h1').a['title']
            link=job.find('h1').a['href']
            firstdescription=job.find('div',style=lambda value: value and 'line-height:18px;font-size:12px; font-family:Verdana, Geneva, sans-serif' in value).p.text
            date=job.find('strong',class_='month').text
            profi=profilescraper(link)
            dict={
                'title':titre,
                'link':link,
                'description':firstdescription,
                'date':date,
                'mission':profi['Mission'],
                'profil':profi['Profil'],
                'dateRemuneration':profi['Date et Remuneration'],
                'email':profi['Email'],
                'cordonnee':profi['Cordonnee']
            }
            list.append(dict)
    
    return(list)
    


# In[13]:


def profilescraper(link):
    profilesTT=requests.get(link)
    src2=BeautifulSoup(profilesTT.content,'html.parser')
    try:
        mission=src2.find('div',class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        mission='NULL'
    try:    
        profil=src2.find('div',class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        profil='NULL'
    try:
        dateetremuneration=src2.find('div',class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        dateetremuneration='NULL'
    try:
        mail=src2.find('div',class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        mail='NULL'
    try:
        cordonnee=src2.find('div',class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        cordonnee='NULL'
        
    profiledict={
        'Mission':mission,
        'Profil':profil,
        'Date et Remuneration':dateetremuneration,
        'Email':mail,
        'Cordonnee':cordonnee
    }
    return profiledict


# In[ ]:

def tuniscraper():
    for lk in listkeyword:
        list=scrapertunitrav(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO tunisietravail(title , link , description , date , mission , profil, dateRemuneration, email,cordonnee,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['description'],l['date'],l['mission'],l['profil'],l['dateRemuneration'],l['email'],l['cordonnee'],lk['keyword'],now)
            try:
                mycursor.execute(sql,values)
                mydb.commit()
            except:
                pass


# In[ ]:




