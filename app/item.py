import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    # when bad request like mismatching type or blank, resolve this problem.
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda i: i['name'] == name, items), 'None')
        # return {'message': item}, 200 if item is not None else 404
        connection = sqlite3.connect('my_app.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        request = cursor.execute(query, (name,))

        row = request.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}
        
        return {"message": "item not found."}, 404

    @jwt_required()
    def post(self, name):
        
        # for item in items:
        #     if item['name'] == name:
        #         print(name + ' already exists.')
        #         return {'message': 'It already exists.'}, 400
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
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

        data = Item.parser.parse_args()
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
        connection = sqlite3.connect('my_app.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)
        rows = result.fetchall()
        items = []
        for row in rows:
            item = {'name': row[0], 'price': row[1]}
            items.append(item)

        return {'items': items}, 200