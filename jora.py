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


def jorascraper(key):
    list=[]
    url='https://tn.jora.com/j?sp=homepage&q=symfony&l='
    url=url.replace('symfony',key)
    jora=requests.get(url)
    print(url)
    src=BeautifulSoup(jora.content,'html.parser')
    jobs=src.find_all('div',class_='job-container result organic-job')
    for job in jobs:
        title=job.find('div',class_='job-item-top-container').text.strip()
        link1=job.find('a',class_='job-item')['href']
        link='https://tn.jora.com'+link1
        company=job.find('div',class_='company-location-container heading-small').span.text.strip()
        location=job.find('span',class_='job-location').text.strip()
        description=job.find('div',class_='job-abstract').text.strip()
        date=job.find('span',class_='job-listed-date heading-xsmall').text.strip()
        more=joraprofi(link)
        dict={
            'title':title,
            'link':link,
            'company':company,
            'location':location,
            'date':date,
            'description':description,
            'more info' :more
        }
        list.append(dict)
    return list


# In[5]:


def joraprofi(link): 
    joraprofile=requests.get(link)
    src2=BeautifulSoup(joraprofile.content,'html.parser')
    try:
        moreinfo=src2.find('div',class_='-desktop-no-padding-top').next_sibling.text.strip()
    except:
        moreinfo='NULL'
    return moreinfo


# In[6]:

def jorascraperr():
    for lk in listkeyword:
        list=jorascraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO jora(title , link , company , location , date , description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['company'],l['location'],l['date'],l['description'],lk['keyword'],now)
            mycursor.execute(sql,values)
            #mydb.commit()


# In[ ]:




