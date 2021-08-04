#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 19:09:26 2021

@author: pranchalsihare
"""

from flask import Flask, request, render_template
from joblib import load

import json
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "cHCF9ShYiMDp1OxU5SdwAZUrYFMD8Jq25a-d6kjtTwxi"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, 
"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})

mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line

app = Flask("__name__")

encode = load('c_encoder.save')
scaler = load('scaler.save')
#model = load('model.save')

def performance(mpg):
    label = ""
    if(mpg<20):
        label = "Low Performance"
    elif(mpg>=20 and mpg<=30):
        label = "Moderate Performance"
    elif(mpg>30):
        label = "High Performance"
    else:
        label = "Unknown"
    return label
    
    
    return label

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/per_predict',methods=['POST'])
def per_predict():
    features = [[x for x in request.form.values()]]
    print(features)
    features[0][-1] = features[0][-1].split()[0] # extracting company name from car name 
    print(features)
    features[0].pop(1) # removing displacement
    print(features)
    print(features[0][-1])
    features[0][-1] = encode.transform([features[0][-1]])
    print(features)
    features = scaler.transform(features)
    print(features)
    payload_scoring = {"input_data": [{"fields": ["cylinders","horsepower","weight","acceleration","model year","origin","car name"], 
"values": features.tolist()}]}
    print(payload_scoring)
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/55248f60-c69a-449d-a7e1-cc4355529d91/predictions?version=2021-08-02', 
    json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring Response")
    predictions = response_scoring.json()
    print(predictions)
    mpg = predictions['predictions'][0]['values'][0][0]
    #mpg = model.predict(features)
    print(mpg)
    per_label = performance(mpg)
    print(per_label)
    return render_template('index.html', prediction_text= 'Car Performance : {label}  \nMiles Per Galon (MPG) : {:.2f}'.format(mpg,label=per_label))

if __name__ == "__main__":
    app.run(debug=True)
    
    