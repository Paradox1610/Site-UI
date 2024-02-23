from flask import Flask
from flask import request
import json
import pickle
import numpy as np
from flask_cors import CORS
import csv
import datetime
import pandas as pd

app = Flask(__name__)
CORS(app)

model = pickle.load(open('heart.pkl','rb'))

a = ["date_time","age","sex","cp","bp","chol","blood sugar","ecg", "max_heart_rate","induced angina","oldpeak","slope of the peak exercise","number major vessels","thal"]

@app.route("/")
def hello_world():
    return "hello world"

@app.route("/ha", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        data = json.loads(request.data) #dictionary format
        arr = []
        for i in data["data_arr"]: 
            arr.append(eval(i)) #converts string elements into ints

        print(arr)

        arr = np.array(arr)
        arr = arr.reshape(1,-1)
        res = model.predict(arr)
        print(res)
        
        if res == [0]:
            return {"res": "You are not on risk of heart disease"}
        else:
            return {"res": "You are on risk of heart disease"}

    return {}

@app.route("/store", methods = ["POST", "GET"])
def store():

    if request.method == "POST":
        data = json.loads(request.data)
        arr = []

        for i in data["data"]: 
            arr.append(eval(i))

        input_data_with_date = [str(datetime.datetime.now())] + arr
        print(input_data_with_date)
        with open("./data.csv", "a") as f:     
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(input_data_with_date)
            f.close()

        return json.dumps({"sucess": True})

@app.route("/show" , methods = ["GET"])
def show():
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        res = list(reader)
        csvfile.close()
        
    return json.dumps({"data" : res})


app.run(port=5000, debug=True)