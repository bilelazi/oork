import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
import pickle
df = pd.read_csv('data_clean.csv')
data = df.dropna()
df = df.drop(labels=range(9999, 10000 ), axis=0)
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
pd.DataFrame(y,columns=multilabel.classes_)
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
final_stopwords_list = stopwords.words('english') + stopwords.words('french')
tfidf = TfidfVectorizer(analyzer='word',max_features=9000,ngram_range=(1,2),stop_words=final_stopwords_list)
X = tfidf.fit_transform(df['Description'].values.astype('U'))
X_train,X_test , y_train ,y_test = train_test_split(X,y , test_size=0.2 , random_state=0)

lr = LogisticRegression(solver='lbfgs',C=22,max_iter=1000,tol=2,class_weight='balanced')
def j_score(y_true , y_pred):
  jacard = np.minimum(y_true,y_pred).sum(axis = 1)/np.maximum(y_true,y_pred).sum(axis = 1)
  return jacard.mean()*100
def Print_Score(y_pred,clf):
  print("Clf: ", clf.__class__.__name__)
  print("Jacard Score : {} ".format(j_score(y_test , y_pred)) )
  print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
  print("---------------------------")
from sklearn.metrics import accuracy_score
for classifier in [lr]:
  clf = OneVsRestClassifier(classifier)
  clf.fit(X_train , y_train,)
  y_pred = clf.predict(X_test)
  Print_Score(y_pred,classifier)


pickle.dump(clf, open("tags_classifier_model.pkl", "wb"))
#joblib.dump(clf, 'tags_classifier_model.pkl')