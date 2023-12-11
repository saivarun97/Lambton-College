import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import clean as cln
from flask_cors import CORS
import json

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
cv = CountVectorizer(stop_words='english')
tv = TfidfVectorizer(stop_words='english')


app=Flask(__name__,template_folder='templates')
CORS(app)
model = pickle.load(open('model.pkl', 'rb'))
count_vec =pickle.load(open('count_vec.pkl', 'rb'))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def vectorize(text):
    df_main = pd.read_csv('df_main.csv')
    X_train = df_main['clean_text']
    cv = CountVectorizer(ngram_range=(1, 6), max_df=1.0, min_df=5)
    cv_train_features = cv.fit_transform(X_train)
    vectorized_text = cv.transform(text)
    return vectorized_text

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    #features = request.form["comment"]
    features = request.get_json()
    sample_review = cln.clean(features['comment'])
    vectotized_sample = count_vec.transform([sample_review])
    prediction = model.predict(vectotized_sample)
    #print(prediction)

    output = prediction[0]
    print(output)
    if output == 0:
        prediction_text = 'The review is not a Spoiler'
        print(prediction_text)
        #return render_template('index.html', prediction_text='The review is not a Spoiler')
        return json.dumps(prediction_text)
        #return prediction_text

    else:
        prediction_text = 'The review is a Spoiler'
        print(prediction_text)
        #return render_template('index.html', prediction_text='The review is a Spoiler')
        return json.dumps(prediction_text)
        #return prediction_text

if __name__ == "__main__":
    app.run(debug=True)
    
