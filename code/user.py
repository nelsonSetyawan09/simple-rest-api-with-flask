import pymysql.cursors
from flask_restful import Resource, reqparse

# we make class User to find user
class User:
    def __init__(self,_id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users` WHERE `username`=%s"
                cursor.execute(sql, (username,))
                row = cursor.fetchone()

        finally:
            connection.close()
            if row:
                user = cls(row['id'], row['username'], row['password'])
            else:
                user = None
            return user

    @classmethod
    def find_by_id(cls, _id):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users` WHERE `id`=%s"
                cursor.execute(sql, (_id,))
                row = cursor.fetchone()

        finally:
            connection.close()
            if row:
                user = cls(*row)   # row['id'], row['username'], row['password']
            else:
                user = None
            return user


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

        if User.find_by_username(data['username']):
            return {'message': 'username have been exist in users'}, 400

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='moliASroot09',
                                     db='test_flask',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`id`, `username`,`password`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (None, data['username'], data['password']))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

        finally:
            connection.close()
        return {"message": "user created successfully!!"}, 201
