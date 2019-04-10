from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:moliASroot09@localhost/test_flask'
# when object change, sqlachemy not change too
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key='citra_amba'
api = Api(app) # make ease to Resource, get-post, get-delete, get-post-delete


db.init_app(app)


@app.before_first_request
def create_tables():
	db.create_all()     # create table in database

# user yang terdaftar login:
    # http://127.0.0.1:5000/auth, method='POST' (otomatis route di buat oleh JWT)
    # pertama, check apa user ada di dlm users list (def authenticate) dlm format json
    # klw ada, return user (id, username, password) di arguments authenticate
    # setelah itu jwt akan menghasilkan token seperti bibawa
    # jwt = {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTI2ODA0NTcsImlhdCI6MTU1MjY4MDE1NywibmJmIjoxNTUyNjgwMTU3LCJpZGVudGl0eSI6MX0.n7Ky_0TWkY2zFPKlBVVIHqO2OeTlTHyacfkaKsF-ItQ" }
    # tiap server di reset(run ulang), jwt token juga reset ulang
    # identity sebagai identitas id dari user yg login (user ada dlm users list)
    # nanti JWT token akan di cocokkan dgn user_id dari identity
jwt = JWT(app, authenticate, identity)


# mirip routes folder di nodejs(maximilliam)
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/chair
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
	app.run(port=5001)

#  export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

























#
