from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
    {'name': 'yeojoy'}
]

class Item(Resource):
    def get(self, name):
        for item in items:
            return jsonify({'item': item})

        return jsonify({'message': 'item not found.'})

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy

app.run(host='0.0.0.0', port=5000)