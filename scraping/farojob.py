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


def nexturl(url,x):
    if x==1:
        url=url+'&paged='+str(x)
    else:
        url=url[:-1]
        url=url+str(x)
    
    return url


# In[5]:


def farojobscraper(key):
    list=[]
    url='https://www.farojob.net/?post_type=noo_job&s=java&type'
    url=url.replace('java',key)
    forajob=requests.get(url)
    src=BeautifulSoup(forajob.content,'lxml')
    for x in range(1,5):
        url=nexturl(url,x)
        print(url)
        jobs=src.find_all('article',class_='loadmore-item')
        for job in jobs:
            title=job.find('h2',class_='loop-item-title').text.strip()
            link=job.find('h2',class_='loop-item-title').a['href']
            try:
                company=job.find('span',class_='hidden').text.strip()
            except:
                company='NULL'
            secteur=job.find('span',class_='job-type').text.strip()
            try:
                location=job.find('em',itemprop="jobLocation").text.strip()
            except:
                location='NULL'
            date=job.find('span',class_='job-date-ago').text.strip()
            datepublication=job.find('time',class_="entry-date").span.text.strip()
            profi=detailscraper(link)
            dict={
                'title':title,
                'link':link,
                'company':company,
                'secteur':secteur,
                'location':location,
                'date':date,
                'datepublication':datepublication,
                'description':profi['detail Post'],
            }
            list.append(dict)


    return list


# In[6]:


def detailscraper(link):
    detail=requests.get(link)
    src2=BeautifulSoup(detail.content,'html.parser')
    try:
        infosurpost=src2.find('div',itemprop="description").text.strip()
    except:
        infosurpost='NULL'
        
    detaidict={
        'detail Post':infosurpost,
    }
    return detaidict


# In[ ]:

def faroscrap():
    for lk in listkeyword:
        list=farojobscraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO farojob(title , link , company , secteur , location , date,datepublication,description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['company'],l['secteur'],l['location'],l['date'],l['datepublication'],l['description'],lk['keyword'],now)
            
            try:
                mycursor.execute(sql,values)
                mydb.commit()
            except:
                pass
               
    

# In[ ]:





# In[ ]:




