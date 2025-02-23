from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import pandas as pd
import requests
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
RENTCAST_URL = 'https://api.rentcast.io/v1/properties'
Llama_Vision_API_KEY = os.getenv("Llama3.2_Vision_API_KEY")
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

def retrievePropertyData(address):
    querystring = {"address" : address}

    headers = {
        "accept": "application/json",
        "X-Api-Key": RENTCAST_API_KEY
    }

    response = requests.get(RENTCAST_URL, headers=headers, params=querystring)

    if response.status_code == 200:
        df = pd.DataFrame(response.json()).drop(columns= ['id','addressLine1','addressLine2','assessorID','legalDescription','owner'])
        return df.text
    else:
        return {"error": f"Failed to fetch data. Status Code: {response.status_code}"}

@app.route("/", methods=["POST"])
def driver():

    address = request.form.get("address")
    damages_context = request.form.get("damagesContext")
    retrofits_context = request.form.get("retrofitsContext")
    images = request.files
    for file in images:
        extension = images[file].filename.split('.')[1]
        images[file].save(os.path.join(UPLOAD_FOLDER, file+"."+extension))
    
    
    

        
if __name__ == "__main__":
    app.run(debug=True)


