from werkzeug.security import safe_str_cmp
from user import User

users=[
    User(1, 'citra', 'asdf')
]

# {'citra': <__main__.User object at 0x7f7b8d29a940>, 'amba': <__main__.User object at 0x7f7b8d29a9b0>}
username_mapping={u.username: u for u in users}

# {1: <__main__.User object at 0x7f7b8d29a940>, 2: <__main__.User object at 0x7f7b8d29a9b0>}
userid_mapping={u.id : u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password): # user.password == password
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id,None)
