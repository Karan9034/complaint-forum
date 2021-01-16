import pandas as pd
import os
import numpy as np
import nltk, random
nltk.download("wordnet","./nltk_data")
nltk.download("wordnet","./nltk_data")
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords,wordnet
from nltk.stem import PorterStemmer
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost
import lightgbm
from sklearn.ensemble import RandomForestClassifier

def Processing_Test (sentence):
    pc=PorterStemmer()
    bb=sentence.lower()
    bb=bb.split()
    bb=[pc.stem(word) for word in bb if word not in set(stopwords.words('english'))]
    sentence =' '.join(bb)
    tf = joblib.load('tfidf.sav')
    l1=[]
    l1.append(sentence)
    X_test = tf.transform(l1).toarray()
    Model1 = joblib.load('xgboost.sav')
    Model2 = joblib.load('rfc.sav')
    Model3 = joblib.load('lightgbm.sav')
    pred1 = Model1.predict(X_test)
    pred2 = Model2.predict(X_test)
    pred3 = Model3.predict(X_test)
    pred=""
    if pred1==pred2 and pred1==pred3:
        pred=pred1
    elif pred1==pred2:
        pred=pred1
    elif pred2==pred3:
        pred=pred2
    elif pred1==pred3:
        pred=pred1
    else:
        pred=pred3
    return pred[0]
