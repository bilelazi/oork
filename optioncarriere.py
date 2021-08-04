#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
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


def OCSraper(key):
    list=[]
    url='https://www.optioncarriere.tn/recherche/emplois?s=symfony&l=Tunisie'
    url=url.replace('symfony',key)
    optioncarriere=requests.get(url)
    print(url)
    src=BeautifulSoup(optioncarriere.content,'html.parser')
    if (not(src.find('div',class_='result-errors'))):
        allul=src.find('ul',class_='jobs')
        jobs=allul.find_all('li')
        for job in jobs:
            try:
                title=job.find('article',class_='job').find('header').find('h2').text.strip()
            except:
                title='NULL'
            try:
                link1=job.find('h2').a['href']
                link='https://www.optioncarriere.tn'+link1
            except:
                link='NULL'
            try:    
                location=job.find('ul',class_='details').li.text.strip()
            except:
                location='NULL'
            try:    
                description=job.find('div',class_='desc').text.strip()
            except:
                description='NULL'
            try:    
                datepub=job.find('ul',class_='tags').li.text.strip()
            except:
                datepub='NULL'
            if(link != 'NULL'):
                profi=profilescraper(link)    
                dict={
                    'title':title,
                    'link':link,
                    'location':location,
                    'description':description,
                    'datepub':datepub,
                    'info1':profi['info1'],
                    'info2':profi['info2'],
                    'info3':profi['info3'],
                    'info4':profi['info4']

                }
                list.append(dict)
    else:
        print('no results founds')


        
    return list


# In[5]:


def profilescraper(link):
    src2=requests.get(link)
    detailepage=BeautifulSoup(src2.content,'html.parser')
    try:
        info1=detailepage.find('ul',class_='details').li.next_sibling.next_sibling.text.strip()
    except:
        info1='NULL'
    try:
        info2=detailepage.find('ul',class_='details').li.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        info2='NULL'
    try:
        info3=detailepage.find('ul',class_='details').li.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        info3='NULL'
    try:
        info4=detailepage.find('section',class_='content').text.strip()
    except:
        info4='NULL'
    dictprofil={    
        'info1':info1,
        'info2':info2,
        'info3':info3,
        'info4':info4
    }

    return dictprofil


# In[6]:


#print('enter keyword')
#key = input('>')
#print(f'processing keyword... : {key}')


# In[8]:

def optionscraper():
    for lk in listkeyword:
        list=OCSraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO optioncarrier(title , link , location , description , datepub , info1 , info2 , info3 , info4,datescraping,keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['location'],l['description'],l['datepub'],l['info1'],l['info2'],l['info3'],l['info4'],now,lk['keyword'])
            try:
                mycursor.execute(sql,values)
                #mydb.commit()
            except:
                pass


# In[ ]:





# In[ ]:




