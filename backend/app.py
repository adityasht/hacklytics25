from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import pandas as pd
import requests
import os
from os import listdir
from os.path import isfile, join
import shutil
import json
from main import retrievePropertyData, main
app = Flask(__name__)
CORS(app)

load_dotenv()
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")



@app.route("/", methods=["POST"])
def driver():

    address = request.form.get("address")
    images = request.files
    property_data =  retrievePropertyData(address)
    for file in images:
        extension = images[file].filename.split('.')[1]
        images[file].save(os.path.join(UPLOAD_FOLDER, file+"."+extension))
    

    image_paths = [f for f in listdir(os.path.join(os.getcwd(), "uploads")) if isfile(join(os.path.join(os.getcwd(), "uploads"), f))]
    final_paths =[f for f in image_paths if "image" in f]
    for path in final_paths:
        main(os.path.join(os.getcwd(), "uploads", path), property_data)
    folder = os.path.join(os.getcwd(), "uploads")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    json_paths = [f for f in listdir(os.path.join(os.getcwd())) if isfile(join(os.path.join(os.getcwd()), f)) and "json" in f]
    print(json_paths)
    responseObj=[]
    for path in json_paths:
        with open(os.path.join(os.getcwd(), path), 'r') as f:
            data = json.load(f)
            print(data.get("final_assessment"))
            responseObj.append(data.get("final_assessment"))
        os.remove(os.path.join(os.getcwd(), path))
    return jsonify(responseObj)

        
if __name__ == "__main__":
    app.run(debug=True)


