from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key='citra_amba'
api = Api(app) # make ease to Resource, get-post, get-delete, get-post-delete


# http://127.0.0.1:5000/auth, method='POST' (otomatis route di buat oleh JWT)
# pertama, check apa user ada di dlm users list (def authenticate)
# klw ada, return user (id, username, password) di arguments authenticate
# setalah itu jwt akan menghasilkan token seperti bibawa
# jwt = {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTI2ODA0NTcsImlhdCI6MTU1MjY4MDE1NywibmJmIjoxNTUyNjgwMTU3LCJpZGVudGl0eSI6MX0.n7Ky_0TWkY2zFPKlBVVIHqO2OeTlTHyacfkaKsF-ItQ" }
# tiap server di reset(run ulang), jwt token juga reset ulang
# identity sebagai identitas id dari user yg login (user ada dlm users list)
# nanti JWT token akan di cocokkan dgn user_id dari identity
jwt = JWT(app, authenticate, identity)


items=[
     {'name': 'chair', 'price': 12.00}
]

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
        item = next(filter(lambda x: x['name'] == name, items), None) # will return first item, if not return None
        return {'item': item}, 200 if item else 404 # versi panjang  200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with {name} already exists'}, 400 # 400 BAD REQUEST

        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201    # 201 is created

    def put(self, name):
        # data = {'price': 190.9} (example)
        data = Item.parser.parse_args()  # return parser with 'json format/like dict' and just have 'price' key
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            # if item above None
            # it will overwrite with item below
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            # update came from dictionary feature, data is dictionary
            # very danger, can be item not have name
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))  # overwrite items global
        return {"message": "item deleted"}


class ItemList(Resource):
    def get(self):
        return {'items': items}



api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')



if __name__ =='__main()__':
    app.run(port=5000, debug=True)




























#
