from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):  # Item.find_by_name(name)
            return {'message': f'An item with {name} already exists'}, 400 # 400 BAD REQUEST

        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key
        # **data == data['price'], data['store_id']
        item = ItemModel(name, data['price'])
        try:
            item.save_update_item_to_db()
        except:
            return {"message": "error, not insert item"},500

        return item.json(), 201    # 201 is created

    def put(self, name):
        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key
        item = ItemModel.find_by_name(name) # dlm bentuk class ItemModel {"name": "chair", "price": 12.90}
        if item:
            item.price=data['price']
        else:
            item = ItemModel(name, data['price'])
        item.save_update_item_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)  # Item.find_by_name(name)
        if item:
            item.delete_item_from_db()
            return {"message": "item deleted"}
        return {"message": f"{name} tidak ada dalam database"}


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
