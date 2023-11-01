from flask import Flask, jsonify, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from pymongo import MongoClient


app = Flask(__name__)

import os
from werkzeug.utils import secure_filename
import bcrypt


app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['db']
users = db['users']
inpcs = db['inpcs']
CORS(app)


@app.route('/users/register', methods=["POST"])
def register():
    users_collection = mongo.db.users
    
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    }

    # Use insert_one to insert a single document
    result = users_collection.insert_one(user_data)

    # Retrieve the _id of the inserted document
    user_id = result.inserted_id

    new_user = users_collection.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    users_collection = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users_collection.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({'token': access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result




UPLOAD_FOLDER = os.path.join(app.root_path, "../ModelAPI/uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/createInpc', methods=['POST'])
def create_inpc():
    inpc_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'category': request.form['category']
    }

    if 'filePdf' in request.files:
        profile_picture = request.files['filePdf']
        if profile_picture.filename != '':
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename))
            inpc_data['filePdf'] = profile_picture_filename

    result = db.inpcs.insert_one(inpc_data)
    return jsonify({'id': str(result.inserted_id), 'msg': "Inpc Added Successfully"})

@app.route('/inpcs', methods=['GET'])
def get_inpcs():
    inpcs = []
    for doc in db.inpcs.find():
        inpcs.append({
            '_id': str(doc['_id']),
            'name': doc['name'],
            'description': doc['description'],
            'category': doc['category'],
            'filePdf': doc.get('filePdf', None)
        })
    return jsonify(inpcs)

@app.route('/inpc/<id>', methods=['GET'])
def getInpc(id):
    inpc = db.inpcs.find_one({'_id': ObjectId(id)})
    return jsonify({
    '_id': str(ObjectId(inpc ['_id'])),
    'name': inpc['name'],

    'description': inpc ['description'],
        'category': inpc ['category'],

    'filePdf': inpc ['filePdf'],
    })

@app.route('/inpcs/<id>', methods=['DELETE'])
def deleteInpc(id):
    db.inpcs.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Inpc Deleted Successfully"})


@app.route('/inpcs/<id>', methods=['PUT'])
def update_inpc(id):
    inpc_data = {
        'name': request.form['name'],

        'description': request.form['description'],
                'category': request.form['category']

    }

    # Handle file upload
    if 'filePdf' in request.files:
        profile_picture = request.files['filePdf']
        if profile_picture.filename != '':
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename))
            inpc_data['filePdf'] = profile_picture_filename

    db.inpcs.update_one({'_id': ObjectId(id)}, {'$set': inpc_data})
    return jsonify({'msg': "Inpc Updated Successfully"})





@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "GET":
        categories = mongo.db.categories.find()
        return jsonify([{"id": str(category["_id"]), "name": category["name"]} for category in categories])

    if request.method == "POST":
        new_category = {"name": request.json["name"]}
        mongo.db.categories.insert_one(new_category)
        return jsonify({"message": "Category created successfully"})

@app.route("/categories/<id>", methods=["GET", "PUT", "DELETE"])
def category(id):
    if request.method == "GET":
        category = mongo.db.categories.find_one({"_id": id})
        if category:
            return jsonify({"id": str(category["_id"]), "name": category["name"]})
        else:
            return jsonify({"message": "Category not found"}), 404

    if request.method == "PUT":
        updated_category = {"name": request.json["name"]}
        mongo.db.categories.update_one({"_id": id}, {"$set": updated_category})
        return jsonify({"message": "Category updated successfully"})

    if request.method == "DELETE":
        mongo.db.categories.delete_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        return jsonify({"message": "Category deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
