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


listkeyword = query()


# In[4]:


def nexturl(url, x):
    if x == 1:
        url = url+'&paged='+str(x)
    else:
        url = url[:-1]
        url = url+str(x)

    return url


# In[5]:


def farojobscraper(key):
    list = []
    url = 'https://www.farojob.net/?post_type=noo_job&s=java&type'
    url = url.replace('java', key)
    forajob = requests.get(url)
    src = BeautifulSoup(forajob.content, 'lxml')
    for x in range(1, 5):
        url = nexturl(url, x)
        print(url)
        jobs = src.find_all('article', class_='loadmore-item')
        for job in jobs:
            title = job.find('h2', class_='loop-item-title').text.strip()
            link = job.find('h2', class_='loop-item-title').a['href']
            try:
                company = job.find('span', class_='hidden').text.strip()
            except:
                company = 'NULL'
            secteur = job.find('span', class_='job-type').text.strip()
            try:
                location = job.find('em', itemprop="jobLocation").text.strip()
            except:
                location = 'NULL'
            date = job.find('span', class_='job-date-ago').text.strip()
            datepublication = job.find(
                'time', class_="entry-date").span.text.strip()
            profi = detailscraper(link)
            dict = {
                'title': title,
                'link': link,
                'company': company,
                'secteur': secteur,
                'location': location,
                'date': date,
                'datepublication': datepublication,
                'description': profi['detail Post'],
            }
            list.append(dict)

    return list


# In[6]:


def detailscraper(link):
    detail = requests.get(link)
    src2 = BeautifulSoup(detail.content, 'html.parser')
    try:
        infosurpost = src2.find('div', itemprop="description").text.strip()
    except:
        infosurpost = 'NULL'

    detaidict = {
        'detail Post': infosurpost,
    }
    return detaidict


# In[ ]:

def faroscrap():
    for lk in listkeyword:
        list = farojobscraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO farojob(title , link , company , secteur , location , date,datepublication,description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['company'], l['secteur'], l['location'],
                      l['date'], l['datepublication'], l['description'], lk['keyword'], now)

            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass


###############################################
################  jora      ###################
###############################################
def jorascraper(key):
    list = []
    url = 'https://tn.jora.com/j?sp=homepage&q=symfony&l='
    url = url.replace('symfony', key)
    jora = requests.get(url)
    print(url)
    src = BeautifulSoup(jora.content, 'html.parser')
    jobs = src.find_all('div', class_='job-container result organic-job')
    for job in jobs:
        title = job.find('div', class_='job-item-top-container').text.strip()
        link1 = job.find('a', class_='job-item')['href']
        link = 'https://tn.jora.com'+link1
        company = job.find(
            'div', class_='company-location-container heading-small').span.text.strip()
        location = job.find('span', class_='job-location').text.strip()
        description = job.find('div', class_='job-abstract').text.strip()
        date = job.find(
            'span', class_='job-listed-date heading-xsmall').text.strip()
        more = joraprofi(link)
        dict = {
            'title': title,
            'link': link,
            'company': company,
            'location': location,
            'date': date,
            'description': description,
            'more info': more
        }
        list.append(dict)
    return list


def joraprofi(link):
    joraprofile = requests.get(link)
    src2 = BeautifulSoup(joraprofile.content, 'html.parser')
    try:
        moreinfo = src2.find(
            'div', class_='-desktop-no-padding-top').next_sibling.text.strip()
    except:
        moreinfo = 'NULL'
    return moreinfo


# In[6]:

def jorascraperr():
    for lk in listkeyword:
        list = jorascraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO jora(title , link , company , location , date , description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['company'], l['location'],
                      l['date'], l['description'], lk['keyword'], now)
            mycursor.execute(sql, values)
            mydb.commit()

###############################################
################  keejob      ###################
###############################################


def keejobscraper(key):
    list = []
    url = 'https://www.keejob.com/offres-emploi/?keywords=java'
    url = url.replace('java', key)
    keejob = requests.get(url)
    src = BeautifulSoup(keejob.content, 'html.parser')
    for x in range(1, 3):
        url = nexturl(url, x)
        print(url)
        jobs = src.find_all('div', class_='block_white_a')
        for job in jobs:
            titre = job.find('div', class_='span8').a.text.strip()
            link1 = job.find('div', class_='span8').a['href']
            link = 'https://www.keejob.com'+link1
            try:
                company = job.find(
                    'div', class_='span12 no-margin-left').a.text
                company = re.sub(r'(\s+|\n)', ' ', company)
            except:
                company = 'NULL'
            datepub = job.find('span', class_='pull-left').text.strip()
            profi = prifilescraper(link)
            dict = {
                'title': titre,
                'link': link,
                'company': company,
                'date': datepub,
                'companyInfo': profi['Company Info'],
                'details': profi['Detail Annonce'],
                'description': profi['description']
            }
            list.append(dict)
        # print(list)

    return list


# In[6]:


def prifilescraper(link):

    keejobdetail = requests.get(link)
    detailpage = BeautifulSoup(keejobdetail.content, 'html.parser')
    try:
        companyinfo = detailpage.find('div', class_='span9 content').text.strip(
        ).replace('\n', '').replace('        ', ' ')
    except:
        companyinfo: 'NULL'
    try:
        detailannonce = detailpage.find('div', class_='text').text.strip().replace(
            '\n', ' ').replace('        ', ' ')
    except:
        detailannonce: 'NULL'
    try:
        description = detailpage.find(
            'div', class_='block_a span12 no-margin-left').p.text
    except:
        description: 'NULL'
    profildict = {
        'Company Info': companyinfo,
        'Detail Annonce': detailannonce,
        'description': description,
    }

    return profildict


# In[8]:

def keescraper():
    for lk in listkeyword:
        list = keejobscraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO keejob(title , link , company , date , companyInfo , details,description,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['company'], l['date'],
                      l['companyInfo'], l['details'], l['description'], lk['keyword'], now)
            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass

###############################################
################  offreemploi      ###################
###############################################


def offreemploi(key):
    list = []
    url = 'https://www.offre-emploi.tn/page/1/?s=java&region&secteur'
    url = url.replace('java', key)
    old_x = '1'
    for x in range(1, 5):
        url = url.replace(old_x, str(x))
        old_x = str(x)
        offreemploi = requests.get(url)
        src = BeautifulSoup(offreemploi.content, 'html.parser')
        print(url)
        jobs = src.find_all('article', class_='js_result_row')
        for job in jobs:
            try:
                titre = job.find('span', itemprop='title').text
            except:
                titre = 'NULL'
            try:
                link = job.find('h2').a['href']
            except:
                link = 'NULL'
            try:
                location = job.find('span', itemprop="name").text
            except:
                location = 'NULL'
            try:
                discrip = job.find('div', itemprop="description").text.strip()
            except:
                discrip = 'NULL'
            try:
                date = job.find('time', itemprop="datePosted").text
            except:
                date = 'NULL'
            if(link != 'NULL'):
                profi = profilscraper(link)
                dict = {
                    'title': titre,
                    'link': link,
                    'location': location,
                    'description': discrip,
                    'date': date,
                    'info1': profi['Detail Info 1'],
                    'info2': profi['Detail Info 2'],
                    'info3': profi['Detail Info 3'],
                    'info4': profi['Detail Info 4'],
                    'info5': profi['Detail Info 5'],
                    'info6': profi['Detail Info 6'],
                    'info7': profi['Detail Info 7']

                }
                449
                list.append(dict)
    return list


# In[5]:


def profilscraper(link):
    detail = requests.get(link)
    src2 = BeautifulSoup(detail.content, 'html.parser')
    try:
        info1 = src2.find(
            'div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info1 = re.sub(r'(\s+|\n)', ' ', info1)
    except:
        info1 = 'NULL'
    try:
        info2 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info2 = re.sub(r'(\s+|\n)', ' ', info2)
    except:
        info2 = 'NULL'
    try:
        info3 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info3 = re.sub(r'(\s+|\n)', ' ', info3)
    except:
        info3 = 'NULL'
    try:
        info4 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info4 = re.sub(r'(\s+|\n)', ' ', info4)
    except:
        info4 = 'NULL'
    try:
        info5 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info5 = re.sub(r'(\s+|\n)', ' ', info5)
    except:
        info5 = 'NULL'
    try:
        info6 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info6 = re.sub(r'(\s+|\n)', ' ', info6)
    except:
        info6 = 'NULL'
    try:
        info7 = src2.find('div', class_='row no-gutter').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.replace('  ', '').strip()
        info7 = re.sub(r'(\s+|\n)', ' ', info7)
    except:
        info7 = 'NULL'
    profildictio = {
        'Detail Info 1': info1,
        'Detail Info 2': info2,
        'Detail Info 3': info3,
        'Detail Info 4': info4,
        'Detail Info 5': info5,
        'Detail Info 6': info6,
        'Detail Info 7': info7,
    }
    return profildictio


# In[ ]:

def emploiscraper():
    for lk in listkeyword:
        list = offreemploi(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO offreemploi(title , link , location , description , date , info1, info2, info3, info4, info5, info6, info7,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['location'], l['description'], l['date'], l['info1'],
                      l['info2'], l['info3'], l['info4'], l['info5'], l['info6'], l['info7'], lk['keyword'], now)
            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass


###############################################
################  talent      ###################
###############################################
def talentscraper(key):
    list = []
    url = 'https://www.talents.tn/listing?location=&latitude=&longitude=&placetype=&placeid=&keywords=java&cat=&subcat='
    url = url.replace('java', key)
    print(url)
    talent = requests.get(url)
    src = BeautifulSoup(talent.content, 'html.parser')
    jobs = src.find(
        'div', class_='listings-container margin-top-35').find_all('div', class_='job-listing')
    for job in jobs:

        title = job.find('h3', class_='job-listing-title').text.strip()
        link = job.find('h3', class_='job-listing-title').a['href']
        company = job.find('h4', class_='job-listing-company').text.strip()
        descr = job.find('p', class_='job-listing-text').text.strip()
        typeemploi = job.find('span', class_='job-type').text.strip()
        footer = job.find('div', class_='job-listing-footer with-icon')
        try:
            loc = footer.find('ul').li.text.strip()
        except:
            loc = 'NULL'
        try:
            salaire = footer.find(
                'ul').li.next_sibling.next_sibling.text.strip()
        except:
            salaire = 'NULL'
        try:
            datepublication = footer.find(
                'ul').li.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        except:
            datepublication = 'NULL'
        profi = profilscraper(link)
        dict = {
            'title': title,
            'link': link,
            'company': company,
            'description': descr,
            'typeemploi': typeemploi,
            'location': loc,
            'salaire': salaire,
            'date': datepublication,
            'info1': profi['info1'],
            'info2': profi['info2'],
            'info3': profi['info3'],
            'info4': profi['info4'],
            'info5': profi['info5'],
            'info6': profi['info6'],
            'info7': profi['info7'],
            'info8': profi['info8'],
            'info9': profi['info9'],
            'info10': profi['info10'],
            'info11': profi['info11'],
            'info12': profi['info12'],
        }
        list.append(dict)

    return list


# In[5]:


def profilscraper(url):
    pagedetail = requests.get(url)
    src2 = BeautifulSoup(pagedetail.content, 'html.parser')
    content = src2.find('div', class_='user-html')
    try:
        info1 = content.find('p').text.strip()
        info1 = re.sub(r'(\s+|\n)', ' ', info1)
    except:
        info1 = 'NULL'
    try:
        info2 = content.find('p').next_sibling.text.strip()
        info2 = re.sub(r'(\s+|\n)', ' ', info2)
    except:
        info2 = 'NULL'
    try:
        info3 = content.find('p').next_sibling.next_sibling.text.strip()
        info3 = re.sub(r'(\s+|\n)', ' ', info3)
    except:
        info3 = 'NULL'
    try:
        info4 = content.find(
            'p').next_sibling.next_sibling.next_sibling.text.strip()
        info4 = re.sub(r'(\s+|\n)', ' ', info4)
    except:
        info4 = 'NULL'
    try:
        info5 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info5 = re.sub(r'(\s+|\n)', ' ', info5)
    except:
        info5 = 'NULL'
    try:
        info6 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info6 = re.sub(r'(\s+|\n)', ' ', info6)
    except:
        info6 = 'NULL'
    try:
        info7 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info7 = re.sub(r'(\s+|\n)', ' ', info7)
    except:
        info7 = 'NULL'
    try:
        info8 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info8 = re.sub(r'(\s+|\n)', ' ', info8)
    except:
        info8 = 'NULL'
    try:
        info9 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info9 = re.sub(r'(\s+|\n)', ' ', info9)
    except:
        info9 = 'NULL'
    try:
        info10 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info10 = re.sub(r'(\s+|\n)', ' ', info10)
    except:
        info10 = 'NULL'
    try:
        info11 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info11 = re.sub(r'(\s+|\n)', ' ', info11)
    except:
        info11 = 'NULL'
    try:
        info12 = content.find(
            'p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
        info12 = re.sub(r'(\s+|\n)', ' ', info12)
    except:
        info12 = 'NULL'

    dictprofil = {
        'info1': info1,
        'info2': info2,
        'info3': info3,
        'info4': info4,
        'info5': info5,
        'info6': info6,
        'info7': info7,
        'info8': info8,
        'info9': info9,
        'info10': info10,
        'info11': info11,
        'info12': info12

    }
    return dictprofil


# In[7]:
def talentscraperr():
    for lk in listkeyword:
        list = talentscraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO talent(title , link , company , description , typeemploi , location, salaire, date, info1, info2, info3, info4, info5, info6, info7, info8, info9, info10, info11, info12,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['company'], l['description'], l['typeemploi'], l['location'], l['salaire'], l['date'], l['info1'], l['info2'],
                      l['info3'], l['info4'], l['info5'], l['info6'], l['info7'], l['info8'], l['info9'], l['info10'], l['info11'], l['info12'], lk['keyword'], now)
            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass

###############################################
################  tanitjob      ###################
###############################################


def tanitscraper(key):
    list = []
    url = 'https://www.tanitjobs.com/jobs/?listing_type%5Bequal%5D=Job&action=search&keywords%5Ball_words%5D=angular&GooglePlace%5Blocation%5D%5Bvalue%5D=&GooglePlace%5Blocation%5D%5Bradius%5D=50'
    url = url.replace('angular', key)
    tanitjob = requests.get(url)
    src = BeautifulSoup(tanitjob.content, 'html.parser')
    for x in range(1, 5):
        url = nexturl(url, x)
        print(url)
        jobs = src.find_all(
            'article', class_='media well listing-item listing-item__jobs')
        for job in jobs:
            titre = job.find(
                'div', class_='media-heading listing-item__title').a.text.strip()
            link = job.find(
                'div', class_='media-heading listing-item__title').a['href']
            date = job.find(
                'div', class_='listing-item__date').text.replace(' ', '')
            loc = job.find('div', class_='listing-item__info clearfix').find('span',
                                                                             class_='listing-item__info--item listing-item__info--item-location').text.strip()
            company = job.find(
                'span', class_='listing-item__info--item listing-item__info--item-company').text.strip()
            profi = profilscraper(link)
            dict = {
                'title': titre,
                'link': link,
                'location': loc,
                'company': company,
                'date': date,
                'description': profi
            }
            list.append(dict)
    return list


# In[6]:


def profilscraper(link):
    src2 = requests.get(
        'https://www.tanitjobs.com/job/792912/sales-executive-%C3%A0-sousse-motoris%C3%A9/?backPage=1&searchID=1617633115.609')
    detailepage = BeautifulSoup(src2.content, 'html.parser')
    description = detailepage.find('div', class_='detail-offre').text.strip()
    description = re.sub(r'(\s+|\n)', ' ', description)
    return description


# In[8]:
def tanitscraperr():
    for lk in listkeyword:
        list = tanitscraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO tanitjob(title , link , location , company , description , date ,keyword ,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['location'], l['company'],
                      l['description'], l['date'], lk['keyword'], now)
            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass

###############################################
################  tunisietravail      ###################
###############################################


def scrapertunitrav(key):
    list = []
    url = 'https://www.tunisietravail.net/search/symfony'
    url = url.replace('symfony', key)
    tunisietravail = requests.get(url)
    src = BeautifulSoup(tunisietravail.content, 'html.parser')
    for x in range(1, 3):
        url = nexturl(url, x)
        print(url)
        jobs = src.find_all('div', style=lambda value: value and 'float:left;width:347px; border:solid 1px #e2e2e2; min-height:250px;margin-top:5px; margin-bottom:5px; margin-right:5px; margin-left:5px;padding-top:5px; padding-bottom:5px; padding-right:5px; padding-left:5px;' in value)
        for job in jobs:
            titre = job.find('h1').a['title']
            link = job.find('h1').a['href']
            firstdescription = job.find(
                'div', style=lambda value: value and 'line-height:18px;font-size:12px; font-family:Verdana, Geneva, sans-serif' in value).p.text
            date = job.find('strong', class_='month').text
            profi = profilescraper(link)
            dict = {
                'title': titre,
                'link': link,
                'description': firstdescription,
                'date': date,
                'mission': profi['Mission'],
                'profil': profi['Profil'],
                'dateRemuneration': profi['Date et Remuneration'],
                'email': profi['Email'],
                'cordonnee': profi['Cordonnee']
            }
            list.append(dict)

    return(list)


# In[13]:


def profilescraper(link):
    profilesTT = requests.get(link)
    src2 = BeautifulSoup(profilesTT.content, 'html.parser')
    try:
        mission = src2.find(
            'div', class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        mission = 'NULL'
    try:
        profil = src2.find(
            'div', class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        profil = 'NULL'
    try:
        dateetremuneration = src2.find(
            'div', class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        dateetremuneration = 'NULL'
    try:
        mail = src2.find('div', class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        mail = 'NULL'
    try:
        cordonnee = src2.find('div', class_='PostContent').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        cordonnee = 'NULL'

    profiledict = {
        'Mission': mission,
        'Profil': profil,
        'Date et Remuneration': dateetremuneration,
        'Email': mail,
        'Cordonnee': cordonnee
    }
    return profiledict


# In[ ]:

def tuniscraper():
    for lk in listkeyword:
        list = scrapertunitrav(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO tunisietravail(title , link , description , date , mission , profil, dateRemuneration, email,cordonnee,keyword,datescraping) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['description'], l['date'], l['mission'],
                      l['profil'], l['dateRemuneration'], l['email'], l['cordonnee'], lk['keyword'], now)
            try:
                mycursor.execute(sql, values)
                mydb.commit()
            except:
                pass

###############################################
################  optioncarrier      ###################
###############################################


def OCSraper(key):
    list = []
    url = 'https://www.optioncarriere.tn/recherche/emplois?s=symfony&l=Tunisie'
    url = url.replace('symfony', key)
    optioncarriere = requests.get(url)
    print(url)
    src = BeautifulSoup(optioncarriere.content, 'html.parser')
    if (not(src.find('div', class_='result-errors'))):
        allul = src.find('ul', class_='jobs')
        jobs = allul.find_all('li')
        for job in jobs:
            try:
                title = job.find('article', class_='job').find(
                    'header').find('h2').text.strip()
            except:
                title = 'NULL'
            try:
                link1 = job.find('h2').a['href']
                link = 'https://www.optioncarriere.tn'+link1
            except:
                link = 'NULL'
            try:
                location = job.find('ul', class_='details').li.text.strip()
            except:
                location = 'NULL'
            try:
                description = job.find('div', class_='desc').text.strip()
            except:
                description = 'NULL'
            try:
                datepub = job.find('ul', class_='tags').li.text.strip()
            except:
                datepub = 'NULL'
            if(link != 'NULL'):
                profi = profilescraper(link)
                dict = {
                    'title': title,
                    'link': link,
                    'location': location,
                    'description': description,
                    'datepub': datepub,
                    'info1': profi['info1'],
                    'info2': profi['info2'],
                    'info3': profi['info3'],
                    'info4': profi['info4']

                }
                list.append(dict)
    else:
        print('no results founds')

    return list


# In[5]:


def profilescraper(link):
    src2 = requests.get(link)
    detailepage = BeautifulSoup(src2.content, 'html.parser')
    try:
        info1 = detailepage.find(
            'ul', class_='details').li.next_sibling.next_sibling.text.strip()
    except:
        info1 = 'NULL'
    try:
        info2 = detailepage.find(
            'ul', class_='details').li.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        info2 = 'NULL'
    try:
        info3 = detailepage.find(
            'ul', class_='details').li.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
    except:
        info3 = 'NULL'
    try:
        info4 = detailepage.find('section', class_='content').text.strip()
    except:
        info4 = 'NULL'
    dictprofil = {
        'info1': info1,
        'info2': info2,
        'info3': info3,
        'info4': info4
    }

    return dictprofil


# In[6]:


#print('enter keyword')
#key = input('>')
#print(f'processing keyword... : {key}')


# In[8]:

def optionscraper():
    for lk in listkeyword:
        list = OCSraper(lk['keyword'])
        mycursor = mydb.cursor()
        now = datetime.now()
        for l in list:
            sql = "INSERT INTO optioncarrier(title , link , location , description , datepub , info1 , info2 , info3 , info4,datescraping,keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (l['title'], l['link'], l['location'], l['description'], l['datepub'],
                      l['info1'], l['info2'], l['info3'], l['info4'], now, lk['keyword'])
            try:
                mycursor.execute(sql, values)
                # mydb.commit()
            except:
                pass
