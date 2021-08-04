from nltk.corpus import stopwords
import pickle
import re
import mysql.connector
import numpy as np
from flask import Flask, render_template, request, signals, url_for
from DataCleaning import *
from scraping import *
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
import nltk
nltk.download('stopwords')


app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jobscraper"
)


tags_classifier_model = open('tags_classifier_model.pkl', 'rb')
clf = pickle.load(tags_classifier_model)


@app.route('/search', methods=['POST'])
def search():
    mycursor = mydb.cursor()

    search = request.form.get('search')
    mycursor.execute(" SELECT * FROM jobsoffers WHERE tags LIKE %(search)s ",
                     {'search': '%' + search + '%'})
    records = mycursor.fetchall()
    mydb.commit()
    return render_template('index.html', records=records)


@app.route('/offre/<offre_id>', methods=['GET'])
def single(offre_id):
    mycursor = mydb.cursor()
    r = "SELECT * FROM jobsoffers WHERE id=%s "
    val = (offre_id,)
    mycursor.execute(r, val)
    offre = mycursor.fetchall()

    return render_template('singlepage.html', offre=offre)


def listoffers():
    mycursor = mydb.cursor()
    req = " SELECT  * from jobsoffers "
    mycursor.execute(req)
    res = mycursor.fetchall()
    list = []
    for r in res:
        dict = {
            'index': r[0],
            'result': r[2]+r[3]
        }
        list.append(dict)
    return list


def save(id, string):
    mycursor = mydb.cursor()
    req = " UPDATE jobsoffers set tags=%s where id=%s "
    val = (string, id)
    mycursor.execute(req, val)
    mydb.commit()


@app.route('/modele')
def modeleing():

    df = pd.read_csv('data_clean.csv')
    data = df.dropna()
    df = df.drop(labels=range(9999, 10000), axis=0)
    df['Description'].iloc[1168]
    type(df['keyword'].iloc[0])
    import ast

    def Convert(string):
        li = list(string.split(" "))
        return li
    df['keyword'] = df['keyword'].apply(lambda x: Convert(x))
    type(df['keyword'].iloc[0])
    df['keyword'].iloc[0]
    y = df['keyword']
    multilabel = MultiLabelBinarizer()
    y = multilabel.fit_transform(df['keyword'])
    multilabel.classes_
    pd.DataFrame(y, columns=multilabel.classes_)
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    final_stopwords_list = stopwords.words(
        'english') + stopwords.words('french')
    tfidf = TfidfVectorizer(analyzer='word', max_features=9000, ngram_range=(
        1, 2), stop_words=final_stopwords_list)
    X = tfidf.fit_transform(df['Description'].values.astype('U'))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)

    lr = LogisticRegression(solver='lbfgs', C=22,
                            max_iter=1000, tol=2, class_weight='balanced')

    def j_score(y_true, y_pred):
        jacard = np.minimum(y_true, y_pred).sum(axis=1) / \
            np.maximum(y_true, y_pred).sum(axis=1)
        return jacard.mean()*100

    def Print_Score(y_pred, clf):
        print("Clf: ", clf.__class__.__name__)
        print("Jacard Score : {} ".format(j_score(y_test, y_pred)))
        print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
        print("---------------------------")
    from sklearn.metrics import accuracy_score
    for classifier in [lr]:
        clf = OneVsRestClassifier(classifier)
        clf.fit(X_train, y_train,)
        y_pred = clf.predict(X_test)
        Print_Score(y_pred, classifier)

    for l in listoffers():
        xt = tfidf.transform([l['result']])
        clf.predict(xt)
        tag = multilabel.inverse_transform(clf.predict(xt))
        string = ",".join(tag[0])
        save(l['index'], string)

    return render_template('index.html')


@app.route('/migration')
def migration():
    mycursor = mydb.cursor()
    req = " SELECT  link , title , description ,date  from farojob "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from jora "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from keejob "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from offreemploi "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from optioncarrier "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from talent "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from tanitjob "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    req = " SELECT  link , title , description ,date  from tunisietravail "
    mycursor.execute(req)
    res = mycursor.fetchall()
    for r in res:
        sql = " INSERT INTO jobsoffers( link , title ,description , date, descriptionclean, titreclean ) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (r[0], r[1], r[2], r[3], r[2], r[1])
        mycursor.execute(sql, values)
        mydb.commit()

    return render_template('index.html')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/admin')
def admin():
    mycursor = mydb.cursor()
    req = """ SELECT * from jobsoffers"""
    mycursor.execute(req)

    data = mycursor.fetchall()
    mycursor.close()
    return render_template('dashboard.html', data=data)


@app.route('/scrap')
def scraping():
    keescraper()
    mycursor = mydb.cursor()
    req = """ SELECT * from keejob"""
    mycursor.execute(req)

    data = mycursor.fetchall()
    mycursor.close()
    return render_template('dashboard.html', data=data)


@app.route('/clean')
def cleaning():
    mycursor = mydb.cursor()
    cleaningg()
    req = """ SELECT * from jobsoffers"""
    mycursor.execute(req)

    data = mycursor.fetchall()
    mycursor.close()
    return render_template('dashboard.html', data=data)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
