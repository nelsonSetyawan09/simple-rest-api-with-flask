from flask_restful import Resource
from models.store import StoreModel


# every Resource must be class
class Store(Resource):

    def get(self, name):
        # Connect to the database
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'An store with {name} already exists'}, 400 # 400 BAD REQUEST

        store = StoreModel(name)
        try:
            store.save_update_item_to_db()
        except:
            return {"message": "error, not insert store"},500
        return store.json(), 201    # 201 is created

    def delete(self, name):
        store = StoreModel.find_by_name(name)  # Item.find_by_name(name)
        if store:
            store.delete_item_from_db()
            return {"message": "store deleted"}
        return {"message": f"{name} store tidak ada dalam database"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
