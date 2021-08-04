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


def nexturl(url,x):
    if x==1:
        url=url+'&page='+str(x)
    else:
        url=url[:-1]
        url=url+str(x)
    
    return url


# In[5]:


def keejobscraper(key):
    list=[]
    url='https://www.keejob.com/offres-emploi/?keywords=java'
    url=url.replace('java',key)
    keejob=requests.get(url)
    src=bs(keejob.content,'html.parser')
    for x in range(1,3):
        url=nexturl(url,x)
        print(url)
        jobs=src.find_all('div',class_='block_white_a')
        for job in jobs:
            titre=job.find('div',class_='span8').a.text.strip()
            link1=job.find('div', class_ ='span8').a['href']
            link='https://www.keejob.com'+link1
            try:
                company=job.find('div', class_='span12 no-margin-left').a.text
                company=re.sub(r'(\s+|\n)',' ',company)
            except:
                company='NULL'
            datepub=job.find('span',class_='pull-left').text.strip()
            profi=prifilescraper(link)
            dict={
                'title':titre,
                'link':link,
                'company':company,
                'date':datepub,
                'companyInfo':profi['Company Info'],
                'details':profi['Detail Annonce'],
                'description':profi['description']
            }
            list.append(dict)
        #print(list)

    return list


# In[6]:


def prifilescraper(link):
    
    keejobdetail=requests.get(link)
    detailpage=bs(keejobdetail.content,'html.parser')
    try:
        companyinfo=detailpage.find('div',class_='span9 content').text.strip().replace('\n','').replace('        ',' ')
    except:
        companyinfo:'NULL'
    try:
        detailannonce=detailpage.find('div',class_='text').text.strip().replace('\n',' ').replace('        ',' ')
    except:
        detailannonce:'NULL'
    try:
        description=detailpage.find('div',class_='block_a span12 no-margin-left').p.text
    except:
        description:'NULL'
    profildict={
        'Company Info':companyinfo,
        'Detail Annonce':detailannonce,
        'description':description,
    }
    
    return profildict


# In[8]:

def keescraper():
    for lk in listkeyword:
        list=keejobscraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO keejob(title , link , company , date , companyInfo , details,description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['company'],l['date'],l['companyInfo'],l['details'],l['description'],lk['keyword'],now)
            try:
                mycursor.execute(sql,values)
                mydb.commit()
            except:
                pass
            


# In[ ]:




