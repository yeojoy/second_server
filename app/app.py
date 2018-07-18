from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # endpoint is /auth

items = [
    {'name': 'good stub', 'price': 13.99}
]

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), 'None')

        return {'message': item}, 200 if item is not None else 404

    @jwt_required()
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

    @jwt_required()
    def put(self, name):
        #data = request.get_json(silent=True)

        #for item in items:
        #    if item['name'] == name:
        #        if item['price'] == data['price']:
        #            return {'message': 'prices are same.'}, 202
        #        else:
        #            item['price'] = data['price']
        #            return {'message': 'updating is success.'}, 200
        #        
        #return {'message': 'item not found'}, 404

        parser = reqparse.RequestParser()
        # when bad request like mismatching type or blank, resolve this problem.
        parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left blank!"
        )

        data = parser.parse_args() # request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item



    @jwt_required()
    def delete(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         items.remove(item)
        #         return {'message': 'success'}, 200
        # 
        # return {'message': 'item not found'}, 404
        
        global items # python thinks items is local variable. so add "global" keyword
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'success to delete item.'}, 200


class ItemList(Resource):
    def get(self):
        return {'items': items}, 200

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy
api.add_resource(ItemList, '/items')

app.run(host='0.0.0.0', port=5000, debug=True)