from flask import Flask
from flask import request
import json
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open('heart.pkl','rb'))


@app.route("/")
def hello_world():
    return "hello world"

@app.route("/ha", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        data = json.loads(request.data)
        arr = []
        for i in data["data_arr"]:
            arr.append(eval(i))

        print(arr)

        arr = np.array(arr)
        arr = arr.reshape(1,-1)
        res = model.predict(arr)
        print(res)
        
        if res == [0]:
            return {"res": "You dont have a heart attack"}
        else:
            return {"res": "You have a heart attack"}

    return {}

app.run(port=5000, debug=True)