from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import url_for
import numpy as np
import joblib

app = Flask(__name__)

model = joblib.load('final_model.sav')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def getPrediction():

    if request.method == 'POST':

        tweet = request.form['myTextBox']
        tweet = [tweet]
        result = model.predict(tweet)

        return redirect(url_for('prediction', output_result=result))

@app.route('/predict/<output_result>')
def prediction(output_result):

    if output_result == [0]:
        type = 'negative'

    elif output_result == [1]:
        type = 'neutral'
        
    else:
        type = 'positive'

    return render_template('index.html', output=type)

if __name__ == '__main__':
    app.run(debug=True)