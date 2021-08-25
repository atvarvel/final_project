# import necessary libraries
import os
from flask import Flask, request, render_template
import numpy as np
import joblib


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#model = joblib.load('model.sav')

@app.route('/')
def home():
    return render_template('index.html')

    
@app.route('/predict/', methods=['GET','POST'])
def predict():
    model_vr = ['very good trip']
    result = model.predict(model_vr)
    print(result)
    
    
    # if request.method == "POST":
        #get form data
       

if __name__ == '__main_':
    app.run(debug=False)
