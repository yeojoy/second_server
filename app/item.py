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
        item = self.find_by_name(name)
        if item:
            return item
        
        return {"message": "item not found."}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('my_app.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        request = cursor.execute(query, (name,))

        row = request.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @jwt_required()
    def post(self, name):
        
        # for item in items:
        #     if item['name'] == name:
        #         print(name + ' already exists.')
        #         return {'message': 'It already exists.'}, 400
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        # items.append(new_item)
        try:
            self.insert(new_item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error
        
        return new_item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("my_app.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price'], ))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("my_app.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name'],))
        connection.commit()
        connection.close()

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
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the itme."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the itme."}, 500

        return updated_item


    @jwt_required()
    def delete(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         items.remove(item)
        #         return {'message': 'success'}, 200
        # 
        # return {'message': 'item not found'}, 404
        
        # global items # python thinks items is local variable. so add "global" keyword
        # items = list(filter(lambda x: x['name'] != name, items))

        connection = sqlite3.connect("my_app.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name, ))
        
        connection.commit()
        connection.close()

        return {'message': 'Item deleted.'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('my_app.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        
        return {'items': items}, 200