import pymysql.cursors
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# every Resource must be class
class Item(Resource):
    parser = reqparse.RequestParser() # take request with reqparse

    # just take argument price, dan if have another argument, diabaikan
    parser.add_argument('price',
        type=float,
        required=True,
        help='field can not be blank!'
    )

    # call first jwt_required before get request
    # postman : di header, pilih Authorization
                # dan di value, input JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTI2ODE4MTUsImlhdCI6MTU1MjY4MTUxNSwibmJmIjoxNTUyNjgxNTE1LCJpZGVudGl0eSI6MX0.n7Ky_0TWkY2zFPKlBVVIHqO2OeTlTHyacfkaKsF-ItQ
    @jwt_required()
    def get(self, name):
        # Connect to the database
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found'}, 404

    @classmethod
    def find_by_name(cls,name): #chair
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `items` WHERE `name` =%s"
                cursor.execute(sql, (name,))
                row = cursor.fetchone() # type dict {"id": 1, "name": "chair", "price": 12.90}
        finally:
            connection.close()
            if row:
                return row  # {"id": 1, "name": "chair", "price": 12.90}

    @classmethod
    def insert_item(cls, item):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                query = "INSERT INTO `items` (`id`, `name`, `price`) VALUES (%s,%s,%s)"
                cursor.execute(query, (None,item['name'], item['price']))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def update_item(cls, item):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                query = "UPDATE  `items` SET `price`=%s WHERE name=%s"
                cursor.execute(query, (item['price'], item['name']))
                connection.commit()
        finally:
            connection.close()

    def post(self, name):
        if self.find_by_name(name):  # Item.find_by_name(name)
            return {'message': f'An item with {name} already exists'}, 400 # 400 BAD REQUEST

        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key
        item = {"name": name, "price": data['price']}
        try:
            self.insert_item(item)
        except:
            return {"message": "error, not insert item"},500

        return item, 201    # 201 is created

    def put(self, name):
        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key
        item_updated = {'name': name, 'price': data['price']}
        if self.find_by_name(name): # {"id": 1, "name": "chair", "price": 12.90}
            try:
                self.update_item(item_updated)
            except:
                return {"message": "not update item from put request"},500
        else:
            try:
                self.insert_item(item_updated)
            except:
                return {"message": "not insert item from put request"},500
        return item_updated

    def delete(self, name):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                query = "DELETE FROM `items` WHERE `name`=%s"
                cursor.execute(query, (name,))
                connection.commit()
        finally:
            connection.close()
        return {"message": "item deleted"}


class ItemList(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                query = "SELECT * FROM `items`"
                cursor.execute(query)
                items = [{'name':row['name'], 'price': float(row['price'])} for row in cursor.fetchall()]
        finally:
            connection.close()
            
        if items:
            return {'items': items},200
        return {"message": "items kosong"}
