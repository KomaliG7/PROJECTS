from flask import Flask,jsonify,redirect,request
from pymongo import MongoClient

from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
Db = client['MYPROJECT']
Collection = Db['Students']

app = Flask(__name__)

@app.route('/')
def home():
    return "welcome to MRECW AIML DEPARTMENT"

@app.route('/getStudents', methods=['GET'])
def get_all_students():
    result=[]
    data=Collection.find()
    for stu in Collection.find():
        stu['_id']=str(stu['_id'])
        result.append(stu)
    return jsonify(result)

@app.route('/addStudents', methods=['POST'])
def add_student():
    data=request.get_json()
    result= Collection.insert_one(data)
    return jsonify({"message": "Students added successfully","id": str(result.inserted_id)}), 201

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    data=request.get_json()
    result= Collection.update_one({"_id":ObjectId(id)},{"$set": data})
    if result.modified_count:
        return jsonify({"message":"Student updated"})
    return jsonify({"error": "update failed"}), 404

@app.route('/deleteStudents/<id>', methods=['DELETE'])
def delete_student(id):
    result= Collection.delete_one({"_id":ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message":"Student deleted"})
    return jsonify({"error": "student not found"}), 404
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)