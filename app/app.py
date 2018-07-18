from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
    {'name': 'good stub', 'price': 13.99}
]

class Item(Resource):

    def get(self, name):
        for item in items:
            if item['name'] == name:
                print("name :" + name)
                return {'item': item}, 200

        return {'message': 'item not found.'}, 404

    def post(self, name):
        new_item = {'name': name, 'price': 12.99}
        items.append(new_item)
        return new_item, 201

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy

app.run(host='0.0.0.0', port=5000)