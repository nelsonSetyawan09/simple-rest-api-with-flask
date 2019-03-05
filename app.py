from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items':[
            {
                'name': 'My Item1',
                'price': 15.99
            }
        ]
    }
] # end stores


@app.route('/')
def home():
    # render_template otomatis look folder templates and render file index.html
    return render_template('index.html')

# use flask request to take data request from user
# and data that take, we use to
@app.route('/store', methods=['POST'])
# name function must be unique
def create_store():
    # get data with format json  came from user in website
    # convert it to format dictionary python
    # and use data to append stores
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)

    # new_store with format dictionary python
    # we convert to format json with jsonify
    # so website can read it
    return jsonify(new_store)


# default methods=['GET']
@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/some_name
def get_store(name):
    # <string:name> same as parameter in get_store
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found!!'})

# get all stores data
# we want send data to website with format json
# we use jsonify from flask framework

@app.route('/store') # http://127.0.0.1:5000/store/some_name
def get_stores():
     # list stores above make it to dictionary
     # so, make jsonify make convert it to json format
     # only type dictionary python can convert to json
    return jsonify({'stores': stores})

# POST /store/:name/item {name:price}
@app.route('/store/<string:name>/item', methods=[POST])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {
        'name': request_data['name'],
        'price': request_data['price']
    }
    for store in stores:
        if store['name'] == name:
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found to make new item!!'})


@app.route('/store/<string:name>/item') # http://127.0.0.1:5000/store/some_name
# many item in store will be get
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})
