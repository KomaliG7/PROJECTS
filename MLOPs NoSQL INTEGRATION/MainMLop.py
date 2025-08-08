from flask import Flask,jsonify,redirect,request
from pymongo import MongoClient
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plp
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder

from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["MLOP"]
data_col = db["cropData"]
metrics_col=db["ModelMetrics"]
predictions_col=db["Predictions"]

app = Flask(__name__)

label_info = {
    0:  {"crop": "APPLE",        "fertilizer": "UREA"},
    1:  {"crop": "BANANA",       "fertilizer": "DAP"},
    2:  {"crop": "BLACK GRAM",   "fertilizer": "DAP"},
    3:  {"crop": "CHICK PEA",    "fertilizer": "UREA"},
    4:  {"crop": "COCONUT",      "fertilizer": "NPK"},
    5:  {"crop": "COFFEE",       "fertilizer": "COMPOST"},
    6:  {"crop": "COTTON",       "fertilizer": "UREA"},
    7:  {"crop": "GRAPES",       "fertilizer": "POTASH"},
    8:  {"crop": "JUTE",         "fertilizer": "NPK"},
    9:  {"crop": "KIDNEY BEANS", "fertilizer": "DAP"},
    10: {"crop": "LENTIL",       "fertilizer": "UREA"},
    11: {"crop": "MAIZE",        "fertilizer": "NPK"},
    12: {"crop": "MANGO",        "fertilizer": "COMPOST"},
    13: {"crop": "MOTHBEANS",    "fertilizer": "DAP"},
    14: {"crop": "MUSKMELON",    "fertilizer": "UREA"},
    15: {"crop": "ORANGE",       "fertilizer": "POTASH"},
    16: {"crop": "PAPAYA",       "fertilizer": "NPK"},
    17: {"crop": "PIGEON PEA",   "fertilizer": "DAP"},
    18: {"crop": "POMEGRANATE",  "fertilizer": "UREA"},
    19: {"crop": "WATERMELON",   "fertilizer": "POTASH"},
    20: {"crop": "RICE",         "fertilizer": "DAP"}
}

@app.route('/')
def home():
    return jsonify({"message":"Welcome to MLO + MongoDB Flask API. Use"})


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    df = pd.read_csv(file)
    df_records = df.to_dict(orient='records')

    data_col.delete_many({})
    data_col.insert_many(df_records)
    df.to_csv("Crop_recommendation.csv",index=False)
    
    return jsonify({"message":"CSV uploaded and stored", "records":len(df_records)})

@app.route('/getData', methods=['GET'])
def get_all_data():
    result=[]
    data=data_col.find()
    for da in data_col.find():
        da['_id']=str(da['_id'])
        result.append(da)
    return jsonify(result)

@app.route('/train',methods=['GET'])
def train_model():
    if not os.path.exists("Crop_recommendation.csv "):
        return jsonify({"error":"CSV file not uploaded yet"}),400

    data=pd.read_csv('Crop_recommendation.csv')
    label_encoder=LabelEncoder()
    data['label']=label_encoder.fit_transform(data['label'])

    x=data.drop('label',axis=1)
    y=data['label']
    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=2,test_size=0.2)
    

    logreg=LogisticRegression(solver='lbfgs',C=1.5,max_iter=300)
    logreg.fit(x_train,y_train)
    y_pred=logreg.predict(x_train)
    cm = confusion_matrix(y_train, y_pred)

    try:
        TP=cm[0][0]
        FP=cm[0][0]
        TN=cm[0][0]
        FN=cm[0][0]
        accuracy=((TP+TN+FN)/(TP+FP+TN+FN))*100
        precision=TP/(TP+FP)*100
        sensitivity=(TP/(TN+FP))*100
        specificity=(TN/(TN+FP))*100
    except:
        return jsonify({"error":"Confusion matrix computation failed"})
    
    metrics_col.delete_many({})
    metrics_col.insert_one({
        "model":"Logistic Regression",
        "TP":int(TP), "FP":int(FP),
        "FN":int(FN), "TN":int(TN),
        "accuracy":accuracy,
        "precision":precision,
        "sensitivity":sensitivity,
        "specificity":specificity
    })
    

    with open("lr.pickle","wb") as f:
        pickle.dump(logreg,f)

    return jsonify({"message":"Model trained and metrics stored succesfully"})


@app.route('/getModelData',methods=['GET'])
def getModelData():
    result=[]
    for da in metrics_col.find():
        da['_id']=str(da['_id'])
        result.append(da)
    return jsonify(da)


@app.route('/predict',methods=['POST'])
def predict():
    input_data=request.get_json()
    expected_fields=['N','P','K','temp','hum','ph','rain']

    if not all(field in input_data for field in expected_fields):
        return jsonify({"error":"Missing fileds in JSON input"}),400
    
    features = np.array([[input_data[field] for field in expected_fields]])

    if not os.path.exists("lr.pickle"):
        return jsonify({"error":"Model not trained yet"}),500
    

    model = pickle.load(open("lr.pickle","rb"))
    prediction = int(model.predict(features)[0])

    crop_info = label_info.get(prediction, {"crop":"UNKNOWN","fertilizer":"UNKNOWN"})

    mongo_data = input_data.copy()
    mongo_data['prediction_label']=prediction
    mongo_data['recommended_crop']=crop_info['crop']
    mongo_data['recommended_fertilizer']=crop_info['fertilizer']

    result = predictions_col.insert_one(mongo_data)

    return jsonify({
        "prediction":prediction,
        "recommended_crop":crop_info['crop'],
        "recommended_fertilizer": crop_info['fertilizer'],
        "mongo_id":str(result.inserted_id),
        "input":input_data
    })                



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)