#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
from datetime import datetime


# In[2]:


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jobscraper"
)


# In[3]:


def query():
    sql = "SELECT * from keywords"
    list=[]
    try:
        mycursor= mydb.cursor()
        mycursor.execute(sql)
        result=mycursor.fetchall()
        for r in result:
            dict={
                'id': r[0],
                'keyword': r[1]
            }
            list.append(dict)

        print(f'successfully')
    except:
        list=[]
    return list

