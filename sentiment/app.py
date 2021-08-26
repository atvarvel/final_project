from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import url_for
import numpy as np
import joblib

app = Flask(__name__)

file = 'sentiment/final_model.sav'

model = joblib.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def getPrediction():

    if request.method == 'POST':

        tweet = request.form['myTextBox']
        tweet_array = [tweet]
        result = model.predict(tweet_array)

        return redirect(url_for('prediction', output_result=result, text=tweet))

@app.route('/predict/<output_result>/<text>', methods=['POST', 'GET'])
def prediction(output_result, text):

    if output_result == '[2]':
        type = 'This tweet has a positive vibe'

    elif output_result == '[1]':
        type = 'This tweet has a neutral vibe'
        
    else:
        type = 'This tweet has a negative vibe'

    return render_template('index.html', output=type, tweet=text)

if __name__ == '__main__':
    app.run(debug=True)