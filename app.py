from flask import Flask, request, jsonify
from bson import ObjectId
from pymongo import MongoClient;

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['spbtMongoApi']
collection = db['users']

@app.route('/api/users', methods=['GET'])
def get_users():

    page = int(request.args.get('page', 0))
    size = int(request.args.get('size', 5))

    data = collection.find().skip(page * size).limit(size)

    results = []

    for item in data:
        results.append({
            'id': str(item['_id']),
            'name': item['name'],
            'email': item['email']
        })

    return jsonify(results)

@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    new_user = {
        'name': user_data['name'],
        'email': user_data['email']
    }

    result = collection.insert_one(new_user)

    if result.inserted_id:
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'message': 'User not created'})

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.json

    update_fields = {
        'name': user_data['name'],
        'email': user_data['email']
    }

    result = collection.update_one({'_id': ObjectId(id)}, {'$set': update_fields})

    if result.modified_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not updated'})

@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': ObjectId(id)})

    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)