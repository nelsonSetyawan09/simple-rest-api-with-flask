from flask_restful import Resource, reqparse
from models.user import UserModel

# we make class User to find user

# mirip controller pada nodejs (maximilliam)
class UserRegister(Resource):
    parser = reqparse.RequestParser() # take request with reqparse (json format here)

    # just take argument username, dan if have another argument, diabaikan
    parser.add_argument('username',
        type=str,
        required=True,
        help='field can not be blank! for username'
    )

    # just take argument password, dan if have another argument, diabaikan
    parser.add_argument('password',
        type=str,
        required=True,
        help='field can not be blank for password!'
    )

    def post(self):
        # recap parser
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'username have been exist in users'}, 400

        user = UserModel(**data) # **data == data['username'], data['password']
        user.save_to_db()
        return {"message": "user created successfully!!"}, 201
