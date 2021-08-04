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


def talentscraper(key):
    list=[]
    url='https://www.talents.tn/listing?location=&latitude=&longitude=&placetype=&placeid=&keywords=java&cat=&subcat='
    url=url.replace('java',key)
    print(url)
    talent=requests.get(url)
    src=BeautifulSoup(talent.content,'html.parser')
    jobs=src.find('div',class_='listings-container margin-top-35').find_all('div',class_='job-listing')   
    for job in jobs:
        
        title=job.find('h3',class_='job-listing-title').text.strip()
        link=job.find('h3',class_='job-listing-title').a['href']
        company=job.find('h4',class_='job-listing-company').text.strip()
        descr=job.find('p',class_='job-listing-text').text.strip()
        typeemploi=job.find('span',class_='job-type').text.strip()
        footer=job.find('div',class_='job-listing-footer with-icon')
        try:
            loc=footer.find('ul').li.text.strip()
        except:
            loc='NULL'
        try:
            salaire=footer.find('ul').li.next_sibling.next_sibling.text.strip()
        except:
            salaire='NULL'
        try:
            datepublication=footer.find('ul').li.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        except:
            datepublication='NULL'
        profi=profilscraper(link)
        dict={
            'title':title,
            'link':link,
            'company':company,
            'description':descr,
            'typeemploi':typeemploi,
            'location':loc,
            'salaire':salaire,
            'date':datepublication,
            'info1':profi['info1'],
            'info2':profi['info2'],
            'info3':profi['info3'],
            'info4':profi['info4'],
            'info5':profi['info5'],
            'info6':profi['info6'],
            'info7':profi['info7'],
            'info8':profi['info8'],
            'info9':profi['info9'],
            'info10':profi['info10'],
            'info11':profi['info11'],
            'info12':profi['info12'],
        }
        list.append(dict)

    return list
    


# In[5]:


def profilscraper(url):
    pagedetail=requests.get(url)
    src2=BeautifulSoup(pagedetail.content,'html.parser')
    content=src2.find('div',class_='user-html')
    try:
        info1=content.find('p').text.strip()
        info1=re.sub(r'(\s+|\n)',' ',info1)
    except:
        info1='NULL'
    try:    
        info2=content.find('p').next_sibling.text.strip()
        info2=re.sub(r'(\s+|\n)',' ',info2)
    except:
        info2='NULL'
    try:
        info3=content.find('p').next_sibling.next_sibling.text.strip()
        info3=re.sub(r'(\s+|\n)',' ',info3)
    except:
        info3='NULL'
    try:
        info4=content.find('p').next_sibling.next_sibling.next_sibling.text.strip()
        info4=re.sub(r'(\s+|\n)',' ',info4)
    except:
        info4='NULL'
    try:
        info5=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info5=re.sub(r'(\s+|\n)',' ',info5)
    except:
        info5='NULL'
    try:
        info6=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info6=re.sub(r'(\s+|\n)',' ',info6)
    except:
        info6='NULL'
    try:
        info7=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info7=re.sub(r'(\s+|\n)',' ',info7)
    except:
        info7='NULL'
    try:
        info8=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info8=re.sub(r'(\s+|\n)',' ',info8)
    except:
        info8='NULL'
    try:
        info9=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info9=re.sub(r'(\s+|\n)',' ',info9)
    except:
        info9='NULL'
    try:
        info10=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info10=re.sub(r'(\s+|\n)',' ',info10)
    except:
        info10='NULL'
    try:
        info11=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info11=re.sub(r'(\s+|\n)',' ',info11)
    except:
        info11='NULL'
    try:
        info12=content.find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info12=re.sub(r'(\s+|\n)',' ',info12)
    except:
        info12='NULL'
    
    dictprofil={
        'info1':info1,
        'info2':info2,
        'info3':info3,
        'info4':info4,
        'info5':info5,
        'info6':info6,
        'info7':info7,
        'info8':info8,
        'info9':info9,
        'info10':info10,
        'info11':info11,
        'info12':info12
        
    }
    return dictprofil


# In[7]:
def talentscraperr():
    for lk in listkeyword:
        list=talentscraper(lk['keyword'])
        mycursor= mydb.cursor()
        now=datetime.now()
        for l in list:
            sql = "INSERT INTO talent(title , link , company , description , typeemploi , location, salaire, date, info1, info2, info3, info4, info5, info6, info7, info8, info9, info10, info11, info12,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(l['title'],l['link'],l['company'],l['description'],l['typeemploi'],l['location'],l['salaire'],l['date'],l['info1'],l['info2'],l['info3'],l['info4'],l['info5'],l['info6'],l['info7'],l['info8'],l['info9'],l['info10'],l['info11'],l['info12'],lk['keyword'],now)
            try:
                mycursor.execute(sql,values)
                mydb.commit()
            except:
                pass


# In[ ]:





# In[ ]:




