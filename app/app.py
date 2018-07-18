from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
    {'name': 'good stub', 'price': 13.99}
]

class Item(Resource):

    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), 'None')

        return {'message': item}, 200 if item is not None else 404

    def post(self, name):
        
        # for item in items:
        #     if item['name'] == name:
        #         print(name + ' already exists.')
        #         return {'message': 'It already exists.'}, 400
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json(silent=True)
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201

    def patch(self, name):
        data = request.get_json(silent=True)
        for item in items:
            if item['name'] == name:
                if item['price'] == data['price']:
                    return {'message': 'prices are same.'}, 202
                else:
                    item['price'] = data['price']
                    return {'message': 'updating is success.'}, 200
                
        return {'message': 'item not found'}, 404

    def delete(self, name):
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': 'success'}, 200
        
        return {'message': 'item not found'}, 404

class ItemList(Resource):
    def get(self):
        return {'items': items}, 200

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy
api.add_resource(ItemList, '/items')

app.run(host='0.0.0.0', port=5000, debug=True)