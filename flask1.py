from flask import Flask, Response, request, jsonify
import pymongo
import json
from bson import ObjectId
from flask.json import JSONEncoder

# send = jsonify
# Response = res.
# request = req

app = Flask(__name__)


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.employee
    mongo.server_info() #trigger exception if can't connect to DB...
    print("MongoDb is connected")

except:
    print("ERROR - can't connect to db")




class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

app.json_encoder = CustomJSONEncoder

# api/v1/employee
@app.route('/api/v1/employee', methods=['POST'])
def create_employee():
    data = request.get_json()  #data = req.body in javascript
    print(data)
    dbResponse = db.employees.insert_one(data)
    inserted_employee = db.employees.find_one({"_id": dbResponse.inserted_id})
    response_data = {
        "status": True,
        "message": "employee created",
        "data": inserted_employee
    }
    return jsonify(response_data)


#  GET Method :=>
@app.route('/api/v1/employees', methods=['GET'])
def get_employees():
    employees = db.employees.find()
    employee_list = []
    for employee in employees:
        employee['_id'] = str(employee['_id'])
        employee_list.append(employee)
    response_data = {
        "status": True,
        "message": "employees retrieved",
        "data": employee_list
    }
    return jsonify(response_data)




@app.route('/api/v1/employee/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()  # data = req.body in javascript
    dbResponse = db.employees.update_one({"_id": ObjectId(employee_id)}, {"$set": data})
    if dbResponse.modified_count == 1:
        updated_employee = db.employees.find_one({"_id": ObjectId(employee_id)})
        response_data = {
            "status": True,
            "message": "employee updated",
            "data": updated_employee
        }
    else:
        response_data = {
            "status": False,
            "message": "employee not found"
        }
    return jsonify(response_data)





@app.route('/api/v1/employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    dbResponse = db.employees.delete_one({"_id": ObjectId(employee_id)})
    if dbResponse.deleted_count == 1:
        response_data = {
            "status": True,
            "message": "employee deleted"
        }
    else:
        response_data = {
            "status": False,
            "message": "employee not found"
        }
    return jsonify(response_data)




if __name__ == '__main__':
    app.run(debug=True)

