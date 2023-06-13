from flask import Flask, jsonify
from pymongo import MongoClient;

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['spbtMongoApi']
collection = db['users']

@app.route('/api/users')
def get_users():
    data = collection.find()
    results = []

    for item in data:
        results.append({
            'id': str(item['_id']),
            'name': item['name'],
            'email': item['email']
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
