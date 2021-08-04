import json
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "cHCF9ShYiMDp1OxU5SdwAZUrYFMD8Jq25a-d6kjtTwxi"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, 
"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})

mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": ["cylinders","horsepower","weight","acceleration","model year","origin","car name"], 
"values": [[1.        , 0.45652174, 0.5361497 , 0.23809524, 0.        ,0.        , 0.19444444]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/55248f60-c69a-449d-a7e1-cc4355529d91/predictions?version=2021-08-02', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring)
predictions = response_scoring.json()
print(predictions['predictions'][0]['values'][0][0])
