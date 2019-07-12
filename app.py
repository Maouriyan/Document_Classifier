import os, sys, shutil, time
import re
import _pickle as cPickle
from textblob import Word
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify, render_template,send_from_directory
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import urllib.request
import json
from sklearn.feature_extraction.text import TfidfVectorizer


app = Flask(__name__)



@app.route('/')
def root():
    return render_template('index.html')

@app.route('/images/<Paasbaan>')
def download_file(Paasbaan):
    return send_from_directory(app.config['images'], Paasbaan)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/work.html')
def work():
    return render_template('work.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/result.html', methods = ['POST'])
def predict():
    model = joblib.load('model/saved_model.pkl')
    print('model loaded')

    if request.method == 'POST':

        f = request.files['file']
        filen = (f.filename)
        f.save(filen)
        print("FIle name is",filen)
        with open('/home/nibi/Desktop/Kaar/FUll/'+filen, 'r') as myfile:
            datta = myfile.read()
        print("Address is",type(f))
        l=[]
        l.append(datta)
        print("THe list is ",l)
        def clean_str(string):
        
            string = re.sub(r"\'s", "", string)
            string = re.sub(r"\'ve", "", string)
            string = re.sub(r"n\'t", "", string)
            string = re.sub(r"\'re", "", string)
            string = re.sub(r"\'d", "", string)
            string = re.sub(r"\'ll", "", string)
            string = re.sub(r",", "", string)
            string = re.sub(r"!", " ! ", string)
            string = re.sub(r"\(", "", string)
            string = re.sub(r"\)", "", string)
            string = re.sub(r"\?", "", string)
            string = re.sub(r"'", "", string)
            string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
            string = re.sub(r"[0-9]\w+|[0-9]","", string)
            string = re.sub(r"\s{2,}", " ", string)
            return string.strip().lower()
        for index,value in enumerate(l):
            print ("processing data:",index)
            l[index] = ' '.join([Word(word).lemmatize() for word in clean_str(value).split()])
        
        #vect = TfidfVectorizer(stop_words='english',min_df=0,max_features=60)
        
        vect = cPickle.load(open("/home/nibi/Desktop/Kaar/FUll/model/vect.pickle","rb"))
        #X = vect.fit_transform(x) 
        #print(X)
        L = vect.transform(l)  
        l_pred = model.predict(L)
        print("Pred is 1",l_pred)
        l_pred = l_pred[0]
        
        print("Pred is 2",l_pred)



    return render_template('result.html', prediction = l_pred)


if __name__ == '__main__':
    app.run(debug = True)
