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
        url=url+'&page='+str(x)
    else:
        url=url[:-1]
        url=url+str(x)
    
    return url


# In[5]:


def tanitscraper(key):
    list=[]
    url='https://www.tanitjobs.com/jobs/?listing_type%5Bequal%5D=Job&action=search&keywords%5Ball_words%5D=angular&GooglePlace%5Blocation%5D%5Bvalue%5D=&GooglePlace%5Blocation%5D%5Bradius%5D=50'
    url=url.replace('angular',key)
    tanitjob=requests.get(url)
    src=BeautifulSoup(tanitjob.content,'html.parser')
    for x in range(1,5):
        url=nexturl(url,x)
        print(url)
        jobs=src.find_all('article', class_ = 'media well listing-item listing-item__jobs')
        for job in jobs:
            titre=job.find('div', class_ ='media-heading listing-item__title').a.text.strip()
            link=job.find('div', class_ ='media-heading listing-item__title').a['href']
            date=job.find('div', class_ = 'listing-item__date').text.replace(' ','')
            loc=job.find('div', class_ ='listing-item__info clearfix').find('span', class_ ='listing-item__info--item listing-item__info--item-location').text.strip()
            company=job.find('span', class_='listing-item__info--item listing-item__info--item-company').text.strip()
            profi=profilscraper(link)
            dict={
                'title':titre,
                'link':link,
                'location':loc,
                'company':company,
                'date':date,
                'description':profi
            }
            list.append(dict)
    return list
        


# In[6]:


def profilscraper(link):
    src2=requests.get('https://www.tanitjobs.com/job/792912/sales-executive-%C3%A0-sousse-motoris%C3%A9/?backPage=1&searchID=1617633115.609')
    detailepage=BeautifulSoup(src2.content,'html.parser')
    description=detailepage.find('div',class_='detail-offre').text.strip()
    description=re.sub(r'(\s+|\n)',' ',description)
    return description  


# In[8]:
def tanitscraperr():
    for lk in listkeyword:
        list=tanitscraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO tanitjob(title , link , location , company , description , date ,keyword ,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['location'],l['company'],l['description'],l['date'],lk['keyword'],now)
            try:
                mycursor.execute(sql,values)
                #mydb.commit()
            except:
                pass


# In[ ]:





# In[ ]:




